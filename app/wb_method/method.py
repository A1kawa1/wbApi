from fastapi import APIRouter, Body, Path, Query, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Annotated

from wb_method.auxiliary import (fetchPositionAutoadvertProduct, fetchSupplierProducts,
                                 fetchFindProductPosition, fetchProductImages,
                                 fetchProductStocks, fetchSearchQuery,
                                 fetchProductPrice, fetchProductFeedbacks)
from wb_method.model import (AutoadvertProduct, FindProductPosition, ProductPrice,
                             ResponseFindProductPosition, ResponseProductImages,
                             ResponseProductFeedbacks, ResponseSupplierProducts,
                             ResponseProductStocks, ResponseSearchQuery,
                             ResponseProductPrice)
from wb_method.example import (responseFindProductPosition, requestFindProductPosition,
                               responseProductImages, responseProductFeedbacks,
                               responseSearchQuery, responseSupplierProducts,
                               responseProductStocks, requestProductPrice,
                               responseProductPrice)


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get('/supplierProducts/{supplier}',
            description='Получение товаров продавца. 20 запросов в минуту',
            responses=responseSupplierProducts)
@limiter.limit('20/minute')
async def supplierProducts(request: Request,
                           supplier: int = Path(description='id продавца', gt=0)):
    result = await fetchSupplierProducts(supplier)

    return JSONResponse(
        ResponseSupplierProducts(
            supplierID=supplier,
            productsAmount=len(result) if not result is None else 0,
            products=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productImages/{nmID}',
            description='Получение изображений из карточки товара. 1 запрос в секунду',
            responses=responseProductImages)
@limiter.limit('1/second')
async def productImages(request: Request,
                        nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductImages(nmID)

    return JSONResponse(
        ResponseProductImages(
            nmID=nmID,
            picsAmount=len(result) if not result is None else 0,
            picsUrls=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productFeedbacks/{nmID}',
            description='Получение отзывов о товаре. 1 запрос в секунду',
            responses=responseProductFeedbacks)
@limiter.limit('1/second')
async def productFeedbacks(request: Request,
                           nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductFeedbacks(nmID)

    return JSONResponse(
        ResponseProductFeedbacks(
            nmID=nmID,
            feedbacksAmount=len(result) if not result is None else 0,
            feedbacks=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productStocks/{nmID}',
            description='Получение остатков товара. 1 запрос в секунду',
            responses=responseProductStocks)
@limiter.limit('1/second')
async def productStocks(request: Request,
                        nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductStocks(nmID)

    return JSONResponse(
        ResponseProductStocks(
            nmID=nmID,
            totalStocks=result[0] if not result is None else 0,
            warehouse=result[1] if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/searchQuery',
            description='Получение нормированного и похожих запросов. 1 запрос в секунду',
            responses=responseSearchQuery)
@limiter.limit('1/second')
async def searchQuery(request: Request,
                      query: str = Query(description='Поисковый запрос', min_length=1)):
    normQuery, similarQueries = await fetchSearchQuery(query)

    return JSONResponse(ResponseSearchQuery(
        query=query,
        normQuery=normQuery,
        similarQueries=similarQueries
    ).model_dump())


@router.post('/findProductPosition/',
             description='Получение позиции товара на первых 5 страницах. 100 запросов в минуту',
             responses=responseFindProductPosition)
@limiter.limit('100/minute')
async def findProductPosition(request: Request,
                              data: Annotated[FindProductPosition, Body(openapi_examples=requestFindProductPosition)]):
    result = await fetchFindProductPosition(
        nmID=data.nmID,
        query=data.query,
        dest=data.dest
    )

    return JSONResponse(
        ResponseFindProductPosition(
            nmID=data.nmID,
            query=data.query,
            position=result if not result is None else -1,
            exists=not result is None
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.post('/positionAutoadvert/',
             description='Получение позиций автоматических рекламных компаний. 50 запросов в минуту')
@limiter.limit('50/minute')
async def positionAutoadvert(request: Request, data: AutoadvertProduct):
    positionAdvert, _ = await fetchPositionAutoadvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(
        {
            'query': data.query,
            'suppliers': data.suppliers,
            'positionAdvert': positionAdvert
        },
        status.HTTP_200_OK if not positionAdvert is None else status.HTTP_400_BAD_REQUEST
    )


@router.post('/positionProducts/',
             description='Получение позиций товаров продавцов. 50 запросов в минуту')
@limiter.limit('50/minute')
async def positionProducts(request: Request, data: AutoadvertProduct):
    _, positionTotal = await fetchPositionAutoadvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(
        {
            'query': data.query,
            'suppliers': data.suppliers,
            'positionTotal': positionTotal
        },
        status.HTTP_200_OK if not positionTotal is None else status.HTTP_400_BAD_REQUEST
    )


@router.post('/productPrice/',
             description='Получение цен товаров. 1 запрос в секунду',
             responses=responseProductPrice)
@limiter.limit('1/second')
async def productPrice(request: Request,
                       data: Annotated[ProductPrice, Body(openapi_examples=requestProductPrice)]):
    result, found = await fetchProductPrice(data.nmID)

    return JSONResponse(
        ResponseProductPrice(
            found=found,
            data=result
        ).model_dump(),
        status.HTTP_200_OK if found else status.HTTP_400_BAD_REQUEST
    )
