from fastapi import FastAPI
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from wb_method.method import router, limiter


app = FastAPI(title='WB Api', version='1.0.0')

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(router, prefix='/api', tags=['Методы WB'])
