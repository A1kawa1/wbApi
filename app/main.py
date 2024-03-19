from fastapi import FastAPI, Request
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from apitally.fastapi import ApitallyMiddleware
from typing import Awaitable, Callable

from methods.method import router, limiter
from limiter.exempt import _request_ctx_var, RT
from config import apitally_id


app = FastAPI(
    title='WB Api',
    version='1.0.0',
    description=('Это сервис предоставляющий необхдимую информацию для автоматизации процесса торговли на WB. '
                 'Ограничения на каждый метод 2 запроса в минуту. '
                 'Для безлимитного доступа и по всем вопросам сотрудничества пишите в telegram @A1kawa')
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    ApitallyMiddleware,
    client_id=apitally_id,
    env='dev'
)

app.include_router(router, prefix='/api', tags=['Методы WB'])


@app.middleware('http')
async def request_context_middleware(
    request: Request, call_next: Callable[..., Awaitable[RT]]
) -> RT:
    try:
        request_ctx = _request_ctx_var.set(request)
        response = await call_next(request)
        _request_ctx_var.reset(request_ctx)
        return response
    except Exception as e:
        raise e
