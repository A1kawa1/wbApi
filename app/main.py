from fastapi import FastAPI

from wb_method.method import router as wb_router

app = FastAPI()
app.include_router(wb_router, prefix='/api', tags=['Методы WB'])
