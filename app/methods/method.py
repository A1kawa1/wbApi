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
                           ResponseFindProductsPositionItem, ResponseFindProductsPosition,
                           ResponseProductImages, ResponseProductFeedbacks,
                           ResponseSupplierProducts, ResponseProductStocks,
                           ResponseSearchQuery, ResponseProductPrice,
                           ResponsePositionAdvert, ResponsePositionProduct)
from methods.example import (responseFindProductPosition, requestFindProductPosition,
                             responseProductImages, responseProductFeedbacks,
                             responseSearchQuery, responseSupplierProducts,
                             responseProductStocks, requestProductPrice,
                             responseProductPrice, requestPositionAdvertProduct,
                             responsePositionAdvert, responsePositionProduct)
from limiter.exempt import exempt_tokens
from limiter.tokens import get_limit_tokens


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.get('/supplierProducts/{supplier}',
            description='Получение товаров продавца.',
            responses=responseSupplierProducts)
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
async def searchQuery(request: Request,
                      query: str = Query(description='Поисковый запрос', min_length=1)):
    normQuery, similarQueries = await fetchSearchQuery(query)

    return JSONResponse(ResponseSearchQuery(
        query=query,
        normQuery=normQuery if not normQuery is None else '',
        similarQueries=similarQueries if not similarQueries is None else []
    ).model_dump())


@router.post('/findProductsPosition',
             description='Получение позиций товаров на первых 10 страницах.',
             responses=responseFindProductPosition)
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
async def findProductsPosition(request: Request,
                              data: Annotated[FindProductPosition, Body(openapi_examples=requestFindProductPosition)]):
    result = await fetchFindProductPosition(
        nmID=data.nmID,
        query=data.query,
        dest=data.dest
    )

    return JSONResponse(
        ResponseFindProductsPosition(
            nmID=data.nmID,
            query=data.query,
            positions=[
                ResponseFindProductsPositionItem(
                    nmID=nmId,
                    position=position
                ).model_dump()
                for nmId, position in result.items()
            ] if not result is None else [],
            exists=not result is None and len(result) > 0
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.post('/positionAdvert',
             description='Получение позиций автоматических рекламных кампаний.',
             responses=responsePositionAdvert)
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
@limiter.limit(get_limit_tokens, exempt_when=exempt_tokens)
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
