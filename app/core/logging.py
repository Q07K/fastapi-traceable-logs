import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from app.core.request_id import get_request_id

logging.basicConfig(level=logging.INFO)


class CustomFormatter(logging.Formatter):
    """Request ID를 자동으로 포함하는 커스텀 포매터"""

    def format(self, record) -> str:
        # 현재 컨텍스트에서 request ID 가져오기
        request_id = get_request_id()
        record.request_id = request_id
        return super().format(record)


FORMAT = CustomFormatter(
    fmt="{asctime} | {levelname:<8} | {request_id} | {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def setup_logging(log_level: str = "DEBUG") -> None:
    """로깅 설정 초기화"""
    # logs 디렉토리 생성
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # 현재 날짜로 파일명 생성
    today = datetime.now().strftime(format="%Y-%m-%d")

    # 루트 로거 설정
    root_logger = logging.getLogger()
    root_logger.setLevel(level=log_level)

    # 미들웨어 로거 설정 (app.middleware)
    middleware_logger = logging.getLogger(name="app.middleware")
    middleware_logger.setLevel(level=logging.INFO)
    middleware_logger.propagate = False  # 루트 로거로 전파 방지

    # 미들웨어용 파일 핸들러
    middleware_file = TimedRotatingFileHandler(
        filename=log_dir / f"{today}.log",
        encoding="utf-8",
    )
    middleware_file.setFormatter(fmt=FORMAT)
    middleware_logger.addHandler(hdlr=middleware_file)

    # 데코레이터 로거 설정 (app.utils)
    utils_logger = logging.getLogger(name="app.utils")
    utils_logger.setLevel(level=logging.DEBUG)
    utils_logger.propagate = False  # 루트 로거로 전파 방지

    # 데코레이터용 파일 핸들러
    utils_file = TimedRotatingFileHandler(
        filename=log_dir / f"{today}-dev.log",
        encoding="utf-8",
    )
    utils_file.setFormatter(fmt=FORMAT)
    utils_logger.addHandler(hdlr=utils_file)


def get_logger(name: str) -> logging.Logger:
    """로거 인스턴스 반환"""
    return logging.getLogger(name=name)
