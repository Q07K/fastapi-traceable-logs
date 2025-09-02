import time
from functools import wraps

from app.core.logging import get_logger

# 'app.utils' 네임스페이스로 로거 가져오기
logger = get_logger(name="app.utils")


def log_function_call(func):
    """함수 호출 및 실행 시간을 로깅하는 데코레이터"""

    @wraps(wrapped=func)
    async def wrapper(*args, **kwargs):
        msg = (
            f"Run: {func.__module__}.{func.__name__}"
            " | "
            f"args: {args}, kwargs: {kwargs}"
        )
        logger.debug(msg=msg)

        try:
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time

            msg = (
                f"Return: {result}"
                " | "
                f"Process Time: {execution_time:.4f} "
            )
            logger.debug(msg=msg)
            return result
        except Exception as e:
            msg = (
                f"Function: {func.__module__}.{func.__name__}"
                " | "
                f"Error Occurred: {e}"
            )
            logger.error(msg=msg, exc_info=True)
            raise

    return wrapper


if __name__ == "__main__":
    # --- 데코레이터 사용 예시 ---

    import asyncio

    @log_function_call
    async def sample_utility_function(a, b):
        """두 숫자를 더하는 간단한 유틸리티 함수"""
        await asyncio.sleep(1)
        return a + b

    # 5번 호출을 하나의 asyncio.run에서 실행
    async def run_multiple_times():
        tasks = [sample_utility_function(a=5, b=i) for i in range(5)]
        _ = await asyncio.gather(*tasks)

    asyncio.run(run_multiple_times())
