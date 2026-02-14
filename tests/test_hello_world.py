import asyncio
import pytest


@pytest.mark.asyncio
async def test_hello_world():
    await asyncio.sleep(0.1)
    assert True
