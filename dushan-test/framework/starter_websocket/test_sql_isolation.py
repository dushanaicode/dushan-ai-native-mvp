import json

import pytest
from websockets.asyncio.client import connect

from fixtures.database_fixtures import TARGETS
from framework.starter_websocket.definitions.constants.websocket_error_codes import (
    WebSocketErrorCodes,
)
from starter_websocket.conftest import ORIGIN


@pytest.mark.parametrize(
    "ws_database_target", TARGETS, ids=lambda target: target["name"], indirect=True
)
@pytest.mark.parametrize("ws_engine", ["uvicorn", "granian"], indirect=True)
async def test_per_recipient_projection_preserves_user_data_scope(socket_case):
    case = socket_case
    _, member = await case.issue(member="m2")
    _, other = await case.issue(member="m3")
    async with (
        connect(case.url(await case.ticket()), origin=ORIGIN, proxy=None) as one,
        connect(case.url(await case.ticket(member)), origin=ORIGIN, proxy=None) as two,
        connect(case.url(await case.ticket(other)), origin=ORIGIN, proxy=None) as three,
    ):
        for websocket in (one, two, three):
            await websocket.recv()
        result = await case.http.post(
            "/api/ws-test/send",
            json={
                "target": {"kind": "audience", "audience": "test"},
                "message": {
                    "type": "records",
                    "payload": {"ids": [1, 2, 3], "names": ["must-not-broadcast"]},
                },
            },
        )
        assert result.status_code == 200, result.text
        names = [
            json.loads(await websocket.recv())["payload"]["names"]
            for websocket in (one, two, three)
        ]
        assert names == [["first-member"], ["second-member"], ["third-member"]]
        await one.send('{"type":"records","payload":{"ids":[1,2,3]},"requestId":"query"}')
        response = json.loads(await one.recv())
        assert response["requestId"] == "query" and response["payload"]["names"] == ["first-member"]
        pool = (await case.http.get("/api/ws-sql/pool")).json()["pools"]["primary"]
        assert pool["leases"] == pool["checked_out"] == 0


@pytest.mark.parametrize(
    "ws_database_target", TARGETS, ids=lambda target: target["name"], indirect=True
)
async def test_sender_without_audience_send_permission_is_rejected(socket_case):
    case = socket_case
    token, _ = await case.issue(member="m2", scopes=frozenset({"read"}))
    _, other = await case.issue(member="m3")
    async with connect(case.url(await case.ticket(other)), origin=ORIGIN, proxy=None) as websocket:
        client_id = json.loads(await websocket.recv())["payload"]["clientId"]
        for target in (
            {"kind": "member", "member_id": "m3"},
            {"kind": "client", "client_id": client_id},
            {"kind": "audience"},
        ):
            result = await case.http.post(
                "/api/ws-sql/send-direct",
                headers={"Authorization": "Bearer " + token},
                json={
                    "target": {"audience": "test", **target},
                    "message": {"type": "echo", "payload": {"text": "unauthorized"}},
                },
            )
            assert (
                result.status_code == 200
                and result.json()["code"] == WebSocketErrorCodes.POLICY.code
            ), result.text
            assert result.json()["data"] is None
        await websocket.send('{"type":"ping"}')
        assert json.loads(await websocket.recv())["type"] == "pong"
