from fastapi import APIRouter, Body, Path, Query, status
from fastapi.responses import JSONResponse
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


@router.get('/supplierProducts/{supplier}', responses=responseSupplierProducts)
async def supplierProducts(supplier: int = Path(description='id продавца', gt=0)):
    result = await fetchSupplierProducts(supplier)

    return JSONResponse(
        ResponseSupplierProducts(
            supplierID=supplier,
            productsAmount=len(result) if not result is None else 0,
            products=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productImages/{nmID}', responses=responseProductImages)
async def productImages(nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductImages(nmID)

    return JSONResponse(
        ResponseProductImages(
            nmID=nmID,
            picsAmount=len(result) if not result is None else 0,
            picsUrls=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productFeedbacks/{nmID}', responses=responseProductFeedbacks)
async def productFeedbacks(nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductFeedbacks(nmID)

    return JSONResponse(
        ResponseProductFeedbacks(
            nmID=nmID,
            feedbacksAmount=len(result) if not result is None else 0,
            feedbacks=result if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/productStocks/{nmID}', responses=responseProductStocks)
async def productStocks(nmID: int = Path(description='id товара', gt=0)):
    result = await fetchProductStocks(nmID)

    return JSONResponse(
        ResponseProductStocks(
            nmID=nmID,
            totalStocks=result[0] if not result is None else 0,
            warehouse=result[1] if not result is None else []
        ).model_dump(),
        status.HTTP_200_OK if not result is None else status.HTTP_400_BAD_REQUEST
    )


@router.get('/searchQuery', responses=responseSearchQuery)
async def searchQuery(query: str = Query(description='Поисковый запрос', min_length=1)):
    normQuery, similarQueries = await fetchSearchQuery(query)

    return JSONResponse(ResponseSearchQuery(
        query=query,
        normQuery=normQuery,
        similarQueries=similarQueries
    ).model_dump())


@router.post('/findProductPosition/', responses=responseFindProductPosition)
async def findProductPosition(data: Annotated[FindProductPosition, Body(openapi_examples=requestFindProductPosition)]):
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


@router.post('/positionAutoadvert/')
async def positionAutoadvert(data: AutoadvertProduct):
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


@router.post('/positionProducts/')
async def positionProducts(data: AutoadvertProduct):
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


@router.post('/productPrice/', responses=responseProductPrice)
async def productPrice(data: Annotated[ProductPrice, Body(openapi_examples=requestProductPrice)]):
    result, found = await fetchProductPrice(data.nmID)

    return JSONResponse(
        ResponseProductPrice(
            found=found,
            data=result
        ).model_dump(),
        status.HTTP_200_OK if found else status.HTTP_400_BAD_REQUEST
    )
