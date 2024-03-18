from fastapi import Request
from contextvars import ContextVar
from typing import TypeVar

from config import DEV_TOKENS


_request_ctx_var: ContextVar[Request] = ContextVar('request_context')
RT = TypeVar('RT')


def get_request_context() -> Request:
    return _request_ctx_var.get()


def exempt_when_dev() -> bool:
    return get_request_context().headers.get('Authorization') in DEV_TOKENS
