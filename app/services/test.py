import asyncio
from typing import Literal

from app.utils.logger import log_function_call


@log_function_call
async def test_service_get() -> Literal[True]:
    await asyncio.sleep(5)
    return True


@log_function_call
async def test_service_post() -> Literal[True]:
    return True
