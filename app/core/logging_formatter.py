"""Custom logging formatter to include request ID in log records."""

import logging
from contextvars import ContextVar

# 요청 ID를 저장하기 위한 컨텍스트 변수
_REQUEST_ID: ContextVar[str] = ContextVar("request_id", default="N/A")


def set_request_id(request_id: str) -> None:
    """현재 컨텍스트에 요청 ID를 설정합니다."""
    _REQUEST_ID.set(request_id)


def get_request_id() -> str:
    """현재 컨텍스트에서 요청 ID를 가져옵니다."""
    return _REQUEST_ID.get()


class CustomFormatter(logging.Formatter):
    """Request ID를 자동으로 포함하는 커스텀 포매터"""

    def format(self, record) -> str:
        # 현재 컨텍스트에서 request ID 가져오기
        request_id = get_request_id()
        record.request_id = request_id
        return super().format(record)
