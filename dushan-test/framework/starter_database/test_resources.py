import asyncio

import pytest
from sqlalchemy import select

from framework.starter_database.connection.connection_factory import ConnectionFactory
from framework.starter_database.exception.database_exception import DatabaseException
from framework.starter_database.session.managed_async_session import ManagedAsyncSession
from framework.starter_database.session.session_provider import SessionProvider


async def test_startup_probe_failure_disposes_created_engine(database_settings, monkeypatch):
    database = SessionProvider(database_settings)
    disposed = []
    from sqlalchemy.ext.asyncio import AsyncEngine

    original_dispose = AsyncEngine.dispose

    async def failing_probe(engine):
        raise OSError("database unavailable")

    async def dispose(engine, *args, **kwargs):
        disposed.append(engine)
        return await original_dispose(engine, *args, **kwargs)

    monkeypatch.setattr(ConnectionFactory, "probe", failing_probe)
    monkeypatch.setattr(AsyncEngine, "dispose", dispose)
    with pytest.raises(DatabaseException):
        async with database.lifespan():
            pytest.fail("unreachable database must not become ready")
    assert len(disposed) == 1 and not database.is_ready


async def test_repeated_cancel_waits_for_actual_session_close(database_case, monkeypatch):
    database, Item, mapper = database_case
    written = asyncio.Event()
    closing = asyncio.Event()
    release = asyncio.Event()
    original = ManagedAsyncSession.close

    async def slow_close(session):
        closing.set()
        await release.wait()
        await original(session)

    monkeypatch.setattr(ManagedAsyncSession, "close", slow_close)

    async def work():
        async with database.transaction():
            await mapper.insert(Item(value="cancelled"))
            written.set()
            await asyncio.Event().wait()

    task = asyncio.create_task(work())
    await written.wait()
    task.cancel()
    await closing.wait()
    try:
        task.cancel()
        await asyncio.sleep(0)
        assert not task.done()
        assert database.get_metrics()["pools"]["primary"]["leases"] == 1
    finally:
        release.set()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert await mapper.count() == 0


async def test_close_waits_for_required_callback_and_rejects_new_operations(database_case):
    database, Item, mapper = database_case
    started = asyncio.Event()
    release = asyncio.Event()

    async def callback():
        started.set()
        await release.wait()
        await mapper.insert(Item(value="callback-during-drain"))

    async def work():
        async with database.transaction():
            database.after_commit(callback)

    task = asyncio.create_task(work())
    await started.wait()
    close = asyncio.create_task(database.close())
    while not database._transactions._draining:
        await asyncio.sleep(0)
    try:
        assert not close.done()
        with pytest.raises(DatabaseException):
            await mapper.count()
    finally:
        release.set()
    await asyncio.wait_for(asyncio.gather(task, close), 3)
    assert not database.is_ready and not database.get_metrics()["pools"]


async def test_background_callback_is_reserved_before_task_starts(database_case):
    database, Item, mapper = database_case
    completed = []

    async def callback():
        await mapper.insert(Item(value="background"))
        completed.append(True)

    database.after_commit(callback, required=False)
    await database.close()
    assert completed == [True]
    assert database.get_metrics()["after_commit"][-1].success


async def test_self_close_is_rejected_without_hanging(database_case):
    database, Item, mapper = database_case
    async with database.transaction():
        with pytest.raises(RuntimeError, match="自身"):
            await database.close()
        await mapper.insert(Item(value="still-active"))
    assert await mapper.count() == 1


async def test_required_callback_cannot_close_its_own_database(database_case):
    database, Item, mapper = database_case

    async def callback():
        with pytest.raises(RuntimeError, match="自身"):
            await database.close()

    async with database.transaction():
        database.after_commit(callback)
    assert database.is_ready


async def test_raw_access_is_forbidden_in_loop_callback_without_task(database_case):
    database, Item, _ = database_case
    async with database.read_session() as session:
        result = await session.execute(select(Item))
        completed = asyncio.get_running_loop().create_future()

        def access():
            try:
                _ = result.raw
            except DatabaseException:
                completed.set_result(True)
            else:
                completed.set_result(False)

        asyncio.get_running_loop().call_soon(access)
        assert await completed
