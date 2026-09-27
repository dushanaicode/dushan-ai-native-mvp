import asyncio
import secrets

import pytest
from fastapi import APIRouter
from starlette.responses import StreamingResponse

from framework.starter_security.definitions.constants.security_error_codes import SecurityErrorCodes
from framework.starter_security.definitions.enums.security_realm import SecurityRealm
from framework.starter_security.exception.security_exception import SecurityException
from framework.starter_security.spi.message_security_provider import MessageSecurityProvider
from framework.starter_web.routing.route_policy import RoutePolicy


class MessageProofs(MessageSecurityProvider):
    """测试的一次性随机证明存储；不是生产 broker 认证或签名实现。"""

    def __init__(self):
        self.proofs = {}
        self.tokens = None

    async def issue(self, session, payload, *, audience):
        proof = secrets.token_bytes(32)
        self.proofs[proof] = (
            session.application_id,
            session.domain,
            audience,
            session.token_digest,
            payload,
        )
        return proof

    async def verify(self, proof, payload, *, application_id, domain, audience):
        value = self.proofs.get(proof)
        if value is None or value[:3] != (application_id, domain, audience) or value[4] != payload:
            raise SecurityException(SecurityErrorCodes.INVALID)
        del self.proofs[proof]
        return await self.tokens.resolve(value[3], application_id=application_id, domain=domain)


async def test_concurrent_requests_and_independent_di_tasks(security_factory):
    async with security_factory() as case:
        credentials = [await case.issue(account_id=f"account-{index}") for index in range(16)]
        responses = await asyncio.gather(*(case.get(token) for token, _ in credentials))
        assert [r.json()["account"] for r in responses] == [
            f"account-{index}" for index in range(16)
        ]
        assert case.service.context.current() is None
        token, _ = credentials[0]

        async def plain_task():
            return case.service.context.current()

        async def secured():
            assert case.service.context.require().account_id == "account-0"
            assert await case.application.tasks.run(plain_task) is None
            assert await case.application.tasks.create_task(plain_task) is None

        await case.service.run(token, RoutePolicy(), secured)
        assert case.service.context.current() is None


async def test_inherited_context_expires_with_parent_scope(security_factory):
    async with security_factory() as case:
        token, _ = await case.issue()
        release = asyncio.Event()

        async def late_child():
            await release.wait()
            return case.service.context.current()

        with case.application.execution():
            async with case.service.authorized(token, RoutePolicy()):
                task = asyncio.create_task(late_child())
            release.set()
            assert await task is None


async def test_multi_application_and_domain_boundaries(security_factory):
    async with (
        security_factory() as first,
        security_factory(
            domains=("admin", "member"), policy=RoutePolicy(domain="member")
        ) as second,
    ):
        first_token, _ = await first.issue()
        second_token, _ = await second.issue(domain="member", account_id="member-1")
        assert (
            first.service is not second.service
            and first.service.tokens is not second.service.tokens
        )
        assert (await second.get(first_token)).json()["code"] == SecurityErrorCodes.INVALID.code
        assert (await second.get(second_token)).json()["account"] == "member-1"
        wrong_domain, _ = await second.issue(domain="admin")
        assert (await second.get(wrong_domain)).json()["code"] == SecurityErrorCodes.INVALID.code
        with first.application.execution():
            async with first.service.authorized(first_token, RoutePolicy()):
                with second.application.execution():
                    assert first.service.context.current() is None


async def test_messages_validate_proof_audience_replay_and_live_session(security_factory):
    messages = MessageProofs()
    policy = RoutePolicy(("read",), realm=SecurityRealm.ACCOUNT)
    async with security_factory(messages=messages) as case:
        messages.tokens = case.service.tokens
        token, session = await case.issue(realm=SecurityRealm.ACCOUNT)

        async def publish():
            return await case.service.issue_message(b"body", audience="billing")

        async def consume(payload):
            assert payload == b"body"
            return case.service.context.require().account_id

        proof = await case.service.run(token, policy, publish)
        with pytest.raises(SecurityException):
            await case.service.run_message(proof, b"tampered", policy, consume, audience="billing")
        with pytest.raises(SecurityException):
            await case.service.run_message(proof, b"body", policy, consume, audience="other")
        assert (
            await case.service.run_message(proof, b"body", policy, consume, audience="billing")
            == "account-1"
        )
        for forged in (proof, b'{"user_id":"root","tenant_id":"tenant-1"}', {"account_id": "root"}):
            with pytest.raises(SecurityException):
                await case.service.run_message(forged, b"body", policy, consume, audience="billing")
        pending = await case.service.run(token, policy, publish)
        await case.change(session, revoked=True)
        with pytest.raises(SecurityException, match="撤销"):
            await case.service.run_message(pending, b"body", policy, consume, audience="billing")
        assert case.service.context.current() is None


async def test_stream_context_lasts_until_complete_response(security_factory):
    router = APIRouter()
    seen = []

    async def stream():
        async def body():
            try:
                seen.append(case.service.context.require().account_id)
                yield b"ok"
                await asyncio.sleep(0)
                seen.append(case.service.context.require().account_id)
            finally:
                seen.append("closed")

        return StreamingResponse(body(), headers={"Content-Length": "2"})

    router.add_api_route("/protected", RoutePolicy()(stream))
    async with security_factory(router=router) as case:
        token, _ = await case.issue()
        assert (await case.get(token)).content == b"ok"
        assert seen == ["account-1", "account-1", "closed"]
        assert case.service.context.current() is None


async def test_message_handler_exception_and_cancellation_release_identity(security_factory):
    messages = MessageProofs()
    policy = RoutePolicy(("read",), realm=SecurityRealm.ACCOUNT)
    async with security_factory(messages=messages) as case:
        messages.tokens = case.service.tokens
        token, _ = await case.issue(realm=SecurityRealm.ACCOUNT)

        async def publish():
            return await case.service.issue_message(b"body", audience="billing")

        async def failed(payload):
            raise ValueError("business failure")

        proof = await case.service.run(token, policy, publish)
        with pytest.raises(ValueError):
            await case.service.run_message(proof, b"body", policy, failed, audience="billing")
        assert case.service.context.current() is None
        entered = asyncio.Event()

        async def blocked(payload):
            entered.set()
            await asyncio.Event().wait()

        proof = await case.service.run(token, policy, publish)
        task = asyncio.create_task(
            case.service.run_message(proof, b"body", policy, blocked, audience="billing")
        )
        await entered.wait()
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert case.service.context.current() is None


async def test_sync_endpoint_receives_only_its_execution_identity(security_factory):
    router = APIRouter()

    def endpoint():
        return {"account": case.service.context.get_current_account_id()}

    router.add_api_route("/protected", RoutePolicy()(endpoint))
    async with security_factory(router=router) as case:
        token, _ = await case.issue(account_id="thread-account")
        assert (await case.get(token)).json() == {"account": "thread-account"}
        assert case.service.context.current() is None
