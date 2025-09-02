import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.logging import get_logger
from app.core.request_id import set_request_id

# 'app.middleware' 네임스페이스로 로거 가져오기
logger = get_logger(name="app.middleware")


class MiddlewareLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 요청 ID 생성
        request_id = str(uuid.uuid4().hex)
        request.state.request_id = request_id

        # 컨텍스트 변수에 요청 ID 설정
        set_request_id(request_id=request_id)

        # User-Agent 헤더 가져오기
        user_agent = request.headers.get("user-agent", default="unknown")

        # 요청 정보 로깅
        start_time = time.time()
        logger.info(
            msg=(
                f"Request: [{request.method}] {request.url}"
                " | "
                f"Client: {request.client.host}"
                " | "
                f"User-Agent: {user_agent}"
            ),
        )

        # 요청 처리
        response = await call_next(request)

        # 응답 로깅
        process_time = time.time() - start_time
        logger.info(
            msg=(
                f"Response: {response.status_code}"
                " | "
                f"Process Time: {process_time:.4f}s"
            ),
        )

        return response
