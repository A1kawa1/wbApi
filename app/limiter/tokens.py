from limiter.exempt import get_request_context
from config import TOKENS, default_limit


def get_limit_tokens():
    token = get_request_context().headers.get('Authorization')
    return TOKENS.get(token, default_limit)
