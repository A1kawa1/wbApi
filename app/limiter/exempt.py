from fastapi import Request
from contextvars import ContextVar
from typing import TypeVar

from config import EXEMPT_TOKENS


_request_ctx_var: ContextVar[Request] = ContextVar('request_context')
RT = TypeVar('RT')


def get_request_context() -> Request:
    return _request_ctx_var.get()


def exempt_tokens() -> bool:
    return get_request_context().headers.get('Authorization') in EXEMPT_TOKENS
