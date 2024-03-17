from pydantic import BaseModel, Field, validator
from typing import List, Dict, Union


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
    nmID: int = Field(description='id товара', gt=0)
    query: str = Field(description='Поисковый запрос', min_length=1)
    dest: int = Field(description='Месторасположение')


class ProductPrice(BaseModel):
    nmID: List[int] = Field(description='Список из id товаров')

    @validator('nmID')
    def check_positive_numbers(cls, value):
        if any(num <= 0 for num in value):
            raise ValueError('The numbers must be greater than zero')
        return value


class Feedbacks(BaseModel):
    valuation: int = Field(description='Оценка')
    text: str = Field(description='Текст отзыва')
    photos: Union[List[str], list] = Field(
        description='Список изображений из отзыва')


class Size(BaseModel):
    optionID: int = Field(description='id размера')
    sizeName: str = Field(description='Название размера')
    sizeOrigName: str = Field(description='Оригинальное название размера')


class SizeProduct(Size):
    ...


class SizePrice(Size):
    salePriceU: int = Field(description='Цена со скидкой')
    salePrice: int = Field(description='Цена без скидки')


class SizeStocks(Size):
    stocks: int = Field(
        description='Кол-во остатков данного размера на текущем складе')


class ElProductPrice(BaseModel):
    productID: int = Field(description='id товара')
    sizes: Union[List[SizePrice], list] = Field(
        description='Список размеров с ценами')


class Product(BaseModel):
    productID: int = Field(description='id товара')
    productName: str = Field(description='Название товара')
    salePriceU: int = Field(description='Цена со скидкой')
    salePrice: int = Field(description='Цена без скидки')
    colors: Union[List[str], list] = Field(description='Список цветов')
    sizes: Union[List[SizeProduct], list] = Field(
        description='Список размеров')


class Warehouse(BaseModel):
    warehouseID: int = Field(description='id скалада')
    warehouseName: str = Field(description='Название склада')
    warehouseStocks: int = Field(
        description='Общее кол-во остатков на данном складе')
    sizes: Union[List[SizeStocks], list] = Field(
        description='Список размеров с остатками')


class ResponseFindProductPosition(BaseModel):
    nmID: int = Field(description='id товара')
    query: str = Field(description='Поисковый запрос')
    exists: bool = Field(description='Найден ли был товар')
    position: int = Field(description='Позиця товара')


class ResponseSupplierProducts(BaseModel):
    supplierID: int = Field(description='id продавца')
    productsAmount: int = Field(description='Кол-во найденных товаров')
    products: Union[List[Product], list] = Field(description='Список товаров')


class ResponseProductImages(BaseModel):
    nmID: int = Field(description='id товара')
    picsAmount: int = Field(description='Кол-во найденных изоражений')
    picsUrls: Union[List[str], list] = Field(
        description='Список ссылок найденных изоражений')


class ResponseProductFeedbacks(BaseModel):
    nmID: int = Field(description='id товара')
    feedbacksAmount: int = Field(description='Кол-во найденных отзывов')
    feedbacks: Union[List[Feedbacks], list] = Field(
        description='Список найденных отзывов')


class ResponseProductStocks(BaseModel):
    nmID: int = Field(description='id товара')
    totalStocks: int = Field(description='Общее кол-во остатков')
    warehouse: Union[List[Warehouse], list] = Field(
        description='Список остатков по складам')


class ResponseSearchQuery(BaseModel):
    query: str = Field(description='Поисковый запрос')
    normQuery: str = Field(description='Нормированный поисковый запрос')
    similarQueries: List[str] = Field(
        description='Список походих поисковых запросов')


class ResponseProductPrice(BaseModel):
    found: bool = Field(
        description='Найдена ли цена хотя бы для одного товара')
    data: List[ElProductPrice] = Field(
        description='Список цен по товарам')
