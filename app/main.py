from fastapi import FastAPI, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import List

from auxiliary import fetchPositionAutoadvertProduct, fetchSupplierProducts, fetchFindProductPosition


class AutoadvertProduct(BaseModel):
    query: str = Field(description='Поисковый запрос', min_length=1)
    suppliers: List[int] = Field(description='Список из id продавцов')
    dest: int = Field(description='Месторасположение')
    page: int = Field(description='Номер страницы', gt=0)

    @validator('suppliers')
    def check_positive_numbers(cls, value):
        if any(num <= 0 for num in value):
            raise ValueError('The numbers must be greater than zero')
        return value


class FindProductPosition(BaseModel):
    query: str = Field(description='Поисковый запрос', min_length=1)
    nmID: int = Field(description='id товара', gt=0)
    dest: int = Field(description='Месторасположение')


app = FastAPI()


@app.post('/api/findProductPosition/')
async def findProductPosition(data: FindProductPosition):
    result = await fetchFindProductPosition(
        query=data.query,
        nmID=data.nmID,
        dest=data.dest
    )

    return JSONResponse({
        'nmID': data.nmID,
        'query': data.query,
        'position': result,
        'exists': not result is None
    })


@app.get('/api/supplierProducts/{supplier}')
async def supplierProducts(supplier: int = Path(description='id продавца', gt=0)):
    result = await fetchSupplierProducts(supplier)

    return JSONResponse({
        'totalCount': len(result) if not result is None else None,
        'data': result
    })


@app.post('/api/positionAutoadvert/')
async def positionAutoadvert(data: AutoadvertProduct):
    positionAdvert, _ = await fetchPositionAutoadvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(positionAdvert)


@app.post('/api/positionProducts/')
async def positionProducts(data: AutoadvertProduct):
    _, positionTotal = await fetchPositionAutoadvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(positionTotal)
