import asyncio

import pytest
from fastapi import APIRouter, Request
from httpx import ASGITransport, AsyncClient
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

from framework.starter_security.public import SecurityErrorCodes, SecurityException
from framework.starter_web.public import RoutePolicy
from framework.starter_web.routing.router_registration import RouterRegistration
from module_system.definitions.constants.public_contexts import PublicContexts

pytestmark = pytest.mark.asyncio(loop_scope="module")


@pytest.fixture(scope="module")
def probes():
    return {"frames": [], "background": [], "entered": asyncio.Event(), "release": asyncio.Event()}


@pytest.fixture(scope="module")
def system_routers(probes):
    router = APIRouter(prefix="/test/public")

    @router.get("/lifecycle")
    @RoutePolicy.public(context=PublicContexts.AUTHENTICATION)
    async def lifecycle(request: Request):
        context = request.app.state.security.context
        frame = context._frame.get()
        probes["frames"].append(frame)
        assert context.current() is None
        assert "system.auth" in context.current_workload().capabilities
        if request.query_params.get("wait") == "yes":
            probes["entered"].set()
            await probes["release"].wait()
        if request.query_params.get("fail") == "yes":
            raise SecurityException(SecurityErrorCodes.DENIED)

        async def background():
            assert context._frame.get() is frame and frame.active
            probes["background"].append(frame)

        return JSONResponse({"ok": True}, background=BackgroundTask(background))

    return (RouterRegistration(router),)


async def test_anonymous_workloads_are_isolated_and_last_through_background(system_app, probes):
    async with AsyncClient(
        transport=ASGITransport(app=system_app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as client:
        task = asyncio.create_task(client.get("/test/public/lifecycle?wait=yes"))
        await asyncio.wait_for(probes["entered"].wait(), 10)
        first = probes["frames"][-1]
        assert (await client.get("/test/public/lifecycle")).json() == {"ok": True}
        assert probes["frames"][-1] is not first
        assert first.active and not probes["frames"][-1].active
        probes["release"].set()
        assert (await task).json() == {"ok": True}
    assert len(probes["background"]) == 2
    assert all(not frame.active for frame in probes["frames"])


async def test_anonymous_workload_cleans_up_on_error_and_cancellation(system_app, probes):
    probes["entered"].clear()
    probes["release"].clear()
    async with AsyncClient(
        transport=ASGITransport(app=system_app),
        base_url="http://testserver",
        headers={"Origin": "http://testserver"},
    ) as client:
        result = await client.get("/test/public/lifecycle?fail=yes")
        assert result.json()["code"] == SecurityErrorCodes.DENIED.code
        assert not probes["frames"][-1].active
        task = asyncio.create_task(client.get("/test/public/lifecycle?wait=yes"))
        await asyncio.wait_for(probes["entered"].wait(), 10)
        frame = probes["frames"][-1]
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task
        assert not frame.active
