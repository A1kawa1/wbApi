from methods.model import (ResponseFindProductPosition, ResponseProductImages,
                             ResponseProductFeedbacks, ResponseSearchQuery,
                             ResponseSupplierProducts, ResponseProductStocks,
                             ResponseProductPrice, ResponsePositionAdvert,
                             ResponsePositionProduct)


requestFindProductPosition = {
    'normal': {
        'summary': 'Пример с корректным артикулом',
        'description': 'Позиция будет найдена',
        'value': {
            'nmID': 17572527,
            'query': 'чехол на iphone 11',
            'dest': -1257786
        },
    },
    'invalid': {
        'summary': 'Пример с некорректным артикулом',
        'description': 'Позиция не будет найдена',
        'value': {
            'nmID': 123,
            'query': 'чехол на iphone 11',
            'dest': -1257786
        },
    },
}


requestProductPrice = {
    'normal': {
        'summary': 'Пример с корректным артикулом',
        'description': 'Позиция будет найдена',
        'value': {
            'nmID': [172033733]
        },
    },
    'invalid': {
        'summary': 'Пример с некорректным артикулом',
        'description': 'Позиция не будет найдена',
        'value': {
            'nmID': [123]
        },
    },
}


responseProductPrice = {
    200: {
        'model': ResponseProductPrice,
        'description': 'Хотя бы один товар был найден',
        'content': {
            'application/json': {
                'example': {
                    "found": True,
                    "data": [
                        {
                            "productID": 172033733,
                            "sizes": [
                                {
                                    "optionID": 285481526,
                                    "name": "41-47",
                                    "origName": "5 ПАР(41-47)",
                                    "salePriceU": 556,
                                    "salePrice": 1200
                                },
                                {
                                    "optionID": 285904341,
                                    "name": "37-41",
                                    "origName": "5 ПАР(37-41)",
                                    "salePriceU": 556,
                                    "salePrice": 1200
                                },
                                {
                                    "optionID": 330497691,
                                    "name": "36-40",
                                    "origName": "2 пары",
                                    "salePriceU": 280,
                                    "salePrice": 550
                                }
                            ]
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponseProductPrice,
        'description': 'Ни один товар не был найден',
        'content': {
            'application/json': {
                'example': {
                    "found": False,
                    "data": [
                        {
                            "productID": 123,
                            "sizes": []
                        }
                    ]
                }
            }
        },
    }
}


responseFindProductPosition = {
    200: {
        'model': ResponseFindProductPosition,
        'description': 'Позиция была найдена',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 17572527,
                    'query': 'чехол на iphone 11',
                    'position': 1,
                    'exists': True
                }
            }
        },
    },
    400: {
        'model': ResponseFindProductPosition,
        'description': 'Позиция не была найдена',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 123,
                    'query': 'чехол на iphone 11',
                    'position': -1,
                    'exists': False
                }
            }
        },
    }
}


responseSupplierProducts = {
    200: {
        'model': ResponseSupplierProducts,
        'description': 'Товары были найдены',
        'content': {
            'application/json': {
                'example': {
                    'supplierID': 435332,
                    'productsAmount': 6,
                    'products': [
                        {
                            'productID': 164481292,
                            'productName': 'Тюль 300х250 см в гостиную спальню кухню',
                            'salePriceU': 570,
                            'salePrice': 1045,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 274006205,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        },
                        {
                            'productID': 145205140,
                            'productName': 'тюль 300х260 см в гостиную спальню на кухню',
                            'salePriceU': 570,
                            'salePrice': 14635,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 244749910,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        },
                        {
                            'productID': 93977558,
                            'productName': 'тюль 300х250 см в гостиную спальню на кухню',
                            'salePriceU': 615,
                            'salePrice': 15780,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 150169941,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        },
                        {
                            'productID': 161223557,
                            'productName': 'Тюль 300х240 на кухню в гостиную спальню',
                            'salePriceU': 615,
                            'salePrice': 15780,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 267899274,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        },
                        {
                            'productID': 90570711,
                            'productName': 'Тюль 300х270 см в гостиную, спальню, на кухню',
                            'salePriceU': 615,
                            'salePrice': 15780,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 145848147,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        },
                        {
                            'productID': 183550898,
                            'productName': 'Тюль вуаль белый в кухню 280х170 см короткий',
                            'salePriceU': 416,
                            'salePrice': 1067,
                            'colors': [
                                'белый'
                            ],
                            'sizes': [
                                {
                                    'optionID': 302566088,
                                    'sizeName': '',
                                    'sizeOrigName': '0'
                                }
                            ]
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponseSupplierProducts,
        'description': 'Товары не были найдены',
        'content': {
            'application/json': {
                'example': {
                    'supplierID': 123,
                    'productsAmount': 0,
                    'products': []
                }
            }
        },
    }
}


responseProductImages = {
    200: {
        'model': ResponseProductImages,
        'description': 'Изображения были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 17572527,
                    'picsAmount': 8,
                    'picsUrls': [
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/1.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/2.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/3.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/4.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/5.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/6.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/7.jpg',
                        'https://basket-02.wbbasket.ru/vol175/part17572/17572527/images/big/8.jpg'
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponseProductImages,
        'description': 'Изображения не были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 123,
                    'picsAmount': 0,
                    'picsUrls': []
                }
            }
        },
    }
}


responseProductFeedbacks = {
    200: {
        'model': ResponseProductFeedbacks,
        'description': 'Отзывы были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 209636218,
                    'feedbacksAmount': 9,
                    'feedbacks': [
                        {
                            'valuation': 1,
                            'text': 'Невозможно вытащить карту из разъема, так как он слишком близко расположен к камере. Только с очень большим усилием получается и если карту согнуть, но это занимает длительное время и пальцы болят потом. Как вернуть товар по браку? \nКак фотографиях товара разъем был на некотором расстоянии от камеры, а по факту впритык.',
                            'photos': [
                                'https://feedback05.wbbasket.ru/vol1688/part168852/168852598/photos/fs.jpg',
                                'https://feedback05.wbbasket.ru/vol1688/part168852/168852599/photos/fs.jpg'
                            ]
                        },
                        {
                            'valuation': 5,
                            'text': 'Айфон 15 про сел как влитой',
                            'photos': [
                                'https://feedback05.wbbasket.ru/vol1705/part170546/170546436/photos/fs.jpg',
                                'https://feedback05.wbbasket.ru/vol1705/part170546/170546441/photos/fs.jpg',
                                'https://feedback05.wbbasket.ru/vol1705/part170546/170546444/photos/fs.jpg',
                                'https://feedback05.wbbasket.ru/vol1705/part170546/170546448/photos/fs.jpg'
                            ]
                        },
                        {
                            'valuation': 4,
                            'text': 'Телефон защищает хорошо! Чехол удобный, качество хорошее.\nВыглядит ужасно, портит вид телефона на 100%, сделан из материала из которого делают недорогие резиновые тапки.',
                            'photos': []
                        },
                        {
                            'valuation': 1,
                            'text': 'Не покупайте данный чехол, не соответствует фото, кормашек под карту просто дырка в чехле, тоесть когда будите вставлять карту будет царапатся телефон',
                            'photos': []
                        },
                        {
                            'valuation': 4,
                            'text': 'Чехол нормальный, но невозможно пользоваться карманом для карт. Вытащить карту невозможно и поэтому возврат.',
                            'photos': []
                        },
                        {
                            'valuation': 5,
                            'text': 'Не очень.  На 15 не смотрится.',
                            'photos': []
                        },
                        {
                            'valuation': 2,
                            'text': 'Карту вообще невозможно достать, мешает ребро камеры',
                            'photos': []
                        },
                        {
                            'valuation': 1,
                            'text': 'Карту не возможно достать',
                            'photos': []
                        },
                        {
                            'valuation': 5,
                            'text': 'Отлично',
                            'photos': []
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponseProductFeedbacks,
        'description': 'Отзывы не были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 123,
                    'feedbacksAmount': 0,
                    'feedbacks': []
                }
            }
        },
    }
}


responseProductStocks = {
    200: {
        'model': ResponseProductStocks,
        'description': 'Остатки были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 214473315,
                    'totalStocks': 1,
                    'warehouse': [
                        {
                            'warehouseID': 507,
                            'warehouseName': 'Коледино WB',
                            'warehouseStocks': 1,
                            'sizes': [
                                {
                                    'optionID': 342359461,
                                    'name': '5XL',
                                    'origName': '5XL',
                                    'stocks': 1
                                }
                            ]
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponseProductStocks,
        'description': 'Остатки не были найдены',
        'content': {
            'application/json': {
                'example': {
                    'nmID': 123,
                    'totalStocks': 0,
                    'warehouse': []
                }
            }
        },
    },
}


responseSearchQuery = {
    200: {
        'model': ResponseSearchQuery,
        'content': {
            'application/json': {
                'example': {
                    'query': 'купить чехол на iphone 11',
                    'normQuery': 'чехол iphone 11',
                    'similarQueries': [
                        'чехол на 11 iphone с принтом',
                        'чехол на 11 iphone с картой',
                        'чехол на 11 iphone прозрачный',
                        'чехол на 11 iphone с квадратными гранями',
                        'чехол на 11 iphone мужской',
                        'чехол на 11 iphone розовый',
                        'чехол на 11 iphone белый',
                        'чехол на 11 iphone черный',
                        'чехол на 11 iphone аниме',
                        'чехол на 11 iphone силиконовый'
                    ]
                }
            }
        },
    }
}


requestPositionAdvertProduct = {
    'normal': {
        'summary': 'Пример с корректными продавцами',
        'description': 'Позиции не будут найдены',
        'value': {
            "query": "чехол на iphone 11",
            "dest": -1257786,
            "page": 1,
            "suppliers": [90788, 519187]
        },
    },
    'invalid': {
        'summary': 'Пример с некорректным продавцами',
        'description': 'Позиции не будут найдены',
        'value': {
            "query": "чехол на iphone 11",
            "dest": -1257786,
            "page": 1,
            "suppliers": [123, 312]
        },
    },
}


responsePositionAdvert = {
    200: {
        'model': ResponsePositionAdvert,
        'description': 'Была найдена хотя бы одна позиция',
        'content': {
            'application/json': {
                'example': {
                    "query": "чехол на iphone 11",
                    "page": 1,
                    "found": True,
                    "positionAdvert": [
                        {
                            "supplierID": 519187,
                            "data": [
                                {
                                    "productID": 118260932,
                                    "position": {
                                        "activeAdvert": True,
                                        "pagePosition": 4,
                                        "advertPosition": 1,
                                        "type": "search",
                                        "cpm": 155
                                    }
                                }
                            ]
                        },
                        {
                            "supplierID": 90788,
                            "data": [
                                {
                                    "productID": 17572527,
                                    "position": {
                                        "activeAdvert": True,
                                        "pagePosition": 1,
                                        "advertPosition": 1,
                                        "type": "auto",
                                        "cpm": 125
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponsePositionAdvert,
        'description': 'Не было найдено ни одной позиции',
        'content': {
            'application/json': {
                'example': {
                    "query": "чехол на iphone 11",
                    "page": 1,
                    "found": False,
                    "positionAdvert": [
                        {
                            "supplierID": 312,
                            "data": []
                        },
                        {
                            "supplierID": 123,
                            "data": []
                        }
                    ]
                }
            }
        },
    },
}


responsePositionProduct = {
    200: {
        'model': ResponsePositionProduct,
        'description': 'Была найдена хотя бы одна позиция',
        'content': {
            'application/json': {
                'example': {
                    "query": "чехол на iphone 11",
                    "page": 1,
                    "found": True,
                    "positionTotal": [
                        {
                            "supplierID": 519187,
                            "data": [
                                {
                                    "productID": 118260932,
                                    "position": {
                                        "activeAdvert": True,
                                        "pagePosition": 2,
                                        "advertPosition": 1,
                                        "type": "search",
                                        "cpm": 155
                                    }
                                }
                            ]
                        },
                        {
                            "supplierID": 90788,
                            "data": [
                                {
                                    "productID": 17572527,
                                    "position": {
                                        "activeAdvert": True,
                                        "pagePosition": 1,
                                        "advertPosition": 1,
                                        "type": "auto",
                                        "cpm": 125
                                    }
                                },
                                {
                                    "productID": 28789609,
                                    "position": {
                                        "activeAdvert": False,
                                        "pagePosition": 58
                                    }
                                },
                                {
                                    "productID": 43646539,
                                    "position": {
                                        "activeAdvert": False,
                                        "pagePosition": 65
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        },
    },
    400: {
        'model': ResponsePositionProduct,
        'description': 'Не было найдено ни одной позиции',
        'content': {
            'application/json': {
                'example': {
                    "query": "чехол на iphone 11",
                    "page": 1,
                    "found": False,
                    "positionTotal": [
                        {
                            "supplierID": 312,
                            "data": []
                        },
                        {
                            "supplierID": 123,
                            "data": []
                        }
                    ]
                }
            }
        },
    },
}
