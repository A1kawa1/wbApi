from fastapi import APIRouter, Body, Path, Query, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Annotated

from methods.auxiliary import (fetchPositionAdvertProduct, fetchSupplierProducts,
                               fetchFindProductPosition, fetchProductImages,
                               fetchProductStocks, fetchSearchQuery,
                               fetchProductPrice, fetchProductFeedbacks)
from methods.model import (AdvertProduct, FindProductPosition, ProductPrice,
                           ResponseFindProductPosition, ResponseProductImages,
                           ResponseProductFeedbacks, ResponseSupplierProducts,
                           ResponseProductStocks, ResponseSearchQuery,
                           ResponseProductPrice, ResponsePositionAdvert,
                           ResponsePositionProduct)
from methods.example import (responseFindProductPosition, requestFindProductPosition,
                             responseProductImages, responseProductFeedbacks,
                             responseSearchQuery, responseSupplierProducts,
                             responseProductStocks, requestProductPrice,
                             responseProductPrice, requestPositionAdvertProduct,
                             responsePositionAdvert, responsePositionProduct)
from limiter.exempt import exempt_when_dev


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get('/supplierProducts/{supplier}',
            description='Получение товаров продавца.',
            responses=responseSupplierProducts)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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
            description='Получение изображений из карточки товара.',
            responses=responseProductImages)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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
            description='Получение отзывов о товаре.',
            responses=responseProductFeedbacks)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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
            description='Получение остатков товара.',
            responses=responseProductStocks)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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
            description='Получение нормированного и похожих запросов.',
            responses=responseSearchQuery)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
async def searchQuery(request: Request,
                      query: str = Query(description='Поисковый запрос', min_length=1)):
    normQuery, similarQueries = await fetchSearchQuery(query)

    return JSONResponse(ResponseSearchQuery(
        query=query,
        normQuery=normQuery,
        similarQueries=similarQueries
    ).model_dump())


@router.post('/findProductPosition',
             description='Получение позиции товара на первых 10 страницах.',
             responses=responseFindProductPosition)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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


@router.post('/positionAdvert',
             description='Получение позиций автоматических рекламных кампаний.',
             responses=responsePositionAdvert)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
async def positionAdvert(request: Request,
                         data: Annotated[AdvertProduct, Body(openapi_examples=requestPositionAdvertProduct)]):
    positionAdvert, _, found, _ = await fetchPositionAdvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(
        ResponsePositionAdvert(
            query=data.query,
            page=data.page,
            found=found,
            positionAdvert=positionAdvert
        ).model_dump(),
        status.HTTP_200_OK if found else status.HTTP_400_BAD_REQUEST
    )


@router.post('/positionProduct',
             description='Получение позиций товаров продавцов.',
             responses=responsePositionProduct)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
async def positionProduct(request: Request,
                          data: Annotated[AdvertProduct, Body(openapi_examples=requestPositionAdvertProduct)]):
    _, positionTotal, _, found = await fetchPositionAdvertProduct(
        query=data.query,
        dest=data.dest,
        page=data.page,
        suppliers=data.suppliers
    )

    return JSONResponse(
        ResponsePositionProduct(
            query=data.query,
            page=data.page,
            found=found,
            positionTotal=positionTotal
        ).model_dump(),
        status.HTTP_200_OK if found else status.HTTP_400_BAD_REQUEST
    )


@router.post('/productPrice',
             description='Получение цен товаров.',
             responses=responseProductPrice)
@limiter.limit('2/minute', exempt_when=exempt_when_dev)
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
