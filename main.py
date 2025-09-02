from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import setup_logging
from app.middleware.logger import MiddlewareLogger
from app.routers import test


@asynccontextmanager
async def lifespan(_: FastAPI):
    # 시작: 리소스 준비
    setup_logging()

    yield

    # 종료: 리소스 정리


# FastAPI 앱 인스턴스 생성
app = FastAPI(
    title="FastAPI Traceable Logs",
    description="FastAPI 서버에서 요청별 로그 추적 시스템",
    version="1.0.0",
    lifespan=lifespan,
)


# CORS 미들웨어 추가
app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=["*"],  # 프로덕션에서는 구체적인 도메인 지정
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 로깅 미들웨어 추가
app.add_middleware(middleware_class=MiddlewareLogger)

# API 라우터 포함
app.include_router(test.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app=app, host="0.0.0.0", port=8000, reload=True, workers=1)
