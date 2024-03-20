from enum import Enum
import asyncio
import aiohttp
import json
from math import ceil


class URL(Enum):
    wildberries_position_autoadvert = 'https://search.wb.ru/exactmatch/ru/common/v5/search?query={query}&resultset=catalog&sort=popular&curr=rub&dest={dest}&page={page}'
    supplier_products = 'https://catalog.wb.ru/sellers/v2/catalog?dest=-1257786&curr=rub&sort=popular&spp={spp}&supplier={supplier}&page={page}'
    product_info = 'https://card.wb.ru/cards/v2/detail?dest=-1257786&curr=rub&nm={nmID}'
    warehouse_name = 'https://static-basket-01.wbbasket.ru/vol0/data/stores-data.json'
    similar_queries = 'https://similar-queries.wildberries.ru/api/v2/search/query?query={query}&lang=ru'
    feedbacks = 'https://feedbacks{feedbacks}.wb.ru/feedbacks/v1/{root}'
    product_image = 'https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{nmID}/images/big/{pics_number}.jpg'
    feedback_image = 'https://feedback{feedback}.wbbasket.ru/vol{vol}/part{part}/{img}/photos/fs.jpg'


advertType = {
    'b': 'auto',
    'c': 'search'
}
headers = {
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Origin': 'https://www.wildberries.ru',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0 (Edition Yx GX)',
}


def getBasket(vol):
    if 0 <= vol <= 143:
        return '01'
    elif 144 <= vol <= 287:
        return '02'
    elif 288 <= vol <= 431:
        return '03'
    elif 432 <= vol <= 719:
        return '04'
    elif 720 <= vol <= 1007:
        return '05'
    elif 1008 <= vol <= 1061:
        return '06'
    elif 1062 <= vol <= 1115:
        return '07'
    elif 1116 <= vol <= 1169:
        return '08'
    elif 1170 <= vol <= 1313:
        return '09'
    elif 1314 <= vol <= 1601:
        return '10'
    elif 1602 <= vol <= 1655:
        return '11'
    elif 1656 <= vol <= 1919:
        return '12'
    elif 1920 <= vol <= 2045:
        return '13'
    elif 2046 <= vol <= 2189:
        return '14'
    elif 2091 <= vol <= 2405:
        return '15'
    else:
        return '16'


def getFeedback(vol):
    if 0 <= vol <= 431:
        return '01'
    elif 432 <= vol <= 863:
        return '02'
    elif 864 <= vol <= 1199:
        return '03'
    elif 1200 <= vol <= 1535:
        return '04'
    elif 1536 <= vol <= 1919:
        return '05'
    else:
        return '06'


def getPrices(product):
    try:
        prices = []
        for size in product['sizes']:
            if size.get('stocks'):
                salePriceU = size.get('price').get('total') // 100
                salePrice = size.get('price').get('basic') // 100

                prices.append({
                    'optionID': size.get('optionId'),
                    'name': size.get('name'),
                    'origName': size.get('origName'),
                    'salePriceU': salePriceU,
                    'salePrice': salePrice
                })

        return prices
    except:
        return []


def getStocks(product):
    try:
        stocks = 0
        for i in product['sizes']:
            for k in i['stocks']:
                stocks += k['qty']
        return stocks
    except:
        return None


async def fetchWarehouseStocks(product):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(URL.warehouse_name.value) as response:
                text = await response.text()
                warehouse_data = json.loads(text)
                warehouse_name = {warehouse.get('id'): warehouse.get('name')
                                  for warehouse
                                  in warehouse_data}

                result = []
                stocks = {}
                for i in product['sizes']:
                    for k in i['stocks']:
                        if k['wh'] not in stocks:
                            stocks[k['wh']] = {
                                'warehouseName': warehouse_name.get(k.get('wh')),
                                'warehouseStocks': 0,
                                'sizes': []
                            }

                        stocks[k['wh']]['sizes'].append({
                            'optionID': i.get('optionId'),
                            'name': i.get('name'),
                            'origName': i.get('origName'),
                            'stocks': k['qty']
                        })
                        stocks[k['wh']]['warehouseStocks'] += k['qty']

                for warehouse, data in stocks.items():
                    tmp = {'warehouseID': warehouse}
                    tmp.update(data)
                    result.append(tmp)

                return result

    except:
        return None


async def fetchPageSupplierProducts(supplier, page):
    res_products = []
    product_id = []

    print(page)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                URL.supplier_products.value.format(
                spp=0, supplier=supplier, page=page),
                headers=headers) as response:

            if response.status != 200:
                return None

            text = await response.text()
            data = json.loads(text)
            products = data.get('data').get('products')

            if products == []:
                return []

            for product in products:
                colors = [color.get('name')
                          for color in product.get('colors')]

                salePriceU = salePrice = 0
                sizes = []

                for size in product['sizes']:
                    sizes.append({
                        'optionID': size.get('optionId'),
                        'sizeName': size.get('name'),
                        'sizeOrigName': size.get('origName')
                    })
                    if not size.get('price') is None:
                        salePriceU = size.get('price').get('total') // 100
                        salePrice = size.get('price').get('basic') // 100

                res_products.append({
                    'productID': product.get('id'),
                    'productName': product.get('name'),
                    'salePriceU': salePriceU,
                    'salePrice': salePrice,
                    'colors': colors,
                    'sizes': sizes
                })
                product_id.append(product.get('id'))

            return res_products, product_id


async def fetchSupplierProducts(supplier):
    check_count_page = 10
    count_attempts = 1

    while True:
        res_products = []
        product_id = []
        start_page = 1
        error_page = False

        while True:
            end_find = False
            tasks = [fetchPageSupplierProducts(supplier, page)
                     for page
                     in range(start_page, start_page+check_count_page)]
            results = await asyncio.gather(*tasks)

            for res in results:
                if res is None:
                    error_page = True
                    break

                if res == []:
                    end_find = True
                else:
                    for el in res[0]:
                        if el.get('productID') not in res_products:
                            res_products.append(el)

                    product_id.extend(res[1])

            if error_page:
                break

            if end_find:
                break

            start_page += check_count_page

        if count_attempts == 5:
            print(f'{count_attempts} attempts ERROR')
            return None

        if len(res_products) != len(product_id) or error_page:
            count_attempts += 1
            continue

        break

    if not res_products:
        return None

    return res_products


async def fetchPositionAdvertProduct(query, dest, page, suppliers):
    try:
        suppliers = list(set(suppliers))

        res_position_advert = {supplier: {} for supplier in suppliers}
        res_position_total = {supplier: {} for supplier in suppliers}

        result_advert = []
        result_total = []

        for attemp in range(10):
            print(attemp)

            async with aiohttp.ClientSession() as session:
                async with session.get(
                        URL.wildberries_position_autoadvert.value.format(
                        query=query, dest=dest, page=page),
                        headers=headers) as response:

                    if response.status == 200:
                        try:
                            text = await response.text()
                            data = json.loads(text)
                            products = data.get('data').get('products')

                            if len(products) == 1:
                                continue

                            autoadvert = []

                            for pagePosition, el in enumerate(products, 1):
                                supplierId = el.get('supplierId')
                                product_id = el.get('id')

                                if supplierId in suppliers:
                                    res_position_total[supplierId][product_id] = {
                                        'activeAdvert': False,
                                        'pagePosition': 100 * (page - 1) + pagePosition
                                    }

                                if el.get('log'):
                                    autoadvert.append(
                                        (
                                            product_id,
                                            el.get('log').get(
                                                'promoPosition') + 1,
                                            advertType.get(
                                                el.get('log').get('tp')),
                                            el.get('log').get('cpm'),
                                            supplierId
                                        )
                                    )

                        except Exception as e:
                            print(e)
                            # logging.exception(e)

                        advertPos = {
                            'auto': 0,
                            'search': 0
                        }
                        for advert in autoadvert:
                            try:
                                supplierId = advert[-1]
                                type = advert[2]

                                if not type is None:
                                    advertPos[type] += 1

                                if supplierId not in suppliers:
                                    continue

                                product_id = advert[0]
                                pagePosition = advert[1]
                                cpm = advert[3]

                                advertPosition = advertPos.get(type)

                                res_position_advert[supplierId][product_id] = {
                                    'activeAdvert': True,
                                    'pagePosition': pagePosition,
                                    'advertPosition': advertPosition,
                                    'type': type,
                                    'cpm': cpm,
                                }

                                if product_id in res_position_total.get(supplierId):
                                    res_position_total[supplierId][product_id]['activeAdvert'] = True
                                    res_position_total[supplierId][product_id]['advertPosition'] = advertPosition
                                    res_position_total[supplierId][product_id]['type'] = type
                                    res_position_total[supplierId][product_id]['cpm'] = cpm

                            except Exception as e:
                                print(e)
                                # logging.exception(e)
                        break

                    await asyncio.sleep(0.1)

        found_advert, found_total = False, False

        for supplierID, product_data in res_position_advert.items():
            data = []
            for productID, position_data in product_data.items():
                data.append({
                    'productID': productID,
                    'position': position_data
                })

            if data:
                found_advert = True

            result_advert.append({
                'supplierID': supplierID,
                'data': data
            })

        for supplierID, product_data in res_position_total.items():
            data = []
            for productID, position_data in product_data.items():
                data.append({
                    'productID': productID,
                    'position': position_data
                })

            if data:
                found_total = True

            result_total.append({
                'supplierID': supplierID,
                'data': data
            })

        return result_advert, result_total, found_advert, found_total

    except Exception as e:
        print(e)
        # logging.exception(e)
        return None, None


async def fetchFindPageProduct(query, nmID, dest, page):
    print('!!!!!!!!', page)
    for attemp in range(10):
        print(page, attemp)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    URL.wildberries_position_autoadvert.value.format(
                        query=query, page=page, dest=dest),
                    headers=headers) as response:

                if response.status == 200:
                    try:
                        text = await response.text()
                        data = json.loads(text)
                        products = data.get('data').get('products')

                        if len(products) == 1:
                            continue

                        for position, product in enumerate(products, 1):
                            if product.get('id') == nmID:
                                return 100 * (page-1) + position
                    except Exception as e:
                        print(e)
                        # logging.exception(e)
                        continue

                    break

                await asyncio.sleep(0.1)

    return None


async def fetchFindProductPosition(nmID, query, dest):
    try:
        page_count = 10
        tasks = [fetchFindPageProduct(query, nmID, dest, page)
                 for page
                 in range(1, page_count+1)]
        results = await asyncio.gather(*tasks)

        for res in results:
            if not res is None:
                return res

        return None

    except Exception as e:
        print(e)
        # logging.exception(e)
        return None


async def fetchProductImages(nmID):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    URL.product_info.value.format(nmID=nmID),
                    headers=headers) as response:

                text = await response.text()
                data = json.loads(text)

                pics_amount = data.get('data').get('products')[0].get('pics')
                part = nmID // 1000
                vol = part // 100
                basket = getBasket(vol)

                return [URL.product_image.value.format(basket=basket,
                                                       vol=vol,
                                                       part=part,
                                                       nmID=nmID,
                                                       pics_number=pics_number)
                        for pics_number
                        in range(1, pics_amount+1)]

    except:
        return None


async def fetchFeedbacksData(number_feedbacks, root, nmID):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                URL.feedbacks.value.format(
                    feedbacks=number_feedbacks, root=root),
                headers=headers) as response:

            text = await response.text()
            data = json.loads(text)
            feedbacks = data.get('feedbacks')

            if not (feedbacks is None or not feedbacks):
                result_feedbacks = []

                for feedback in feedbacks:
                    if feedback.get('nmId') != nmID:
                        continue

                    photos_tmp = feedback.get('photo')
                    photos = []
                    if not photos_tmp is None:
                        for photo in photos_tmp:
                            part = photo // 1000
                            vol = part // 100

                            photos.append(URL.feedback_image.value.format(
                                feedback=getFeedback(vol),
                                vol=vol,
                                part=part,
                                img=photo
                            ))

                    result_feedbacks.append({
                        'valuation': feedback.get('productValuation'),
                        'text': feedback.get('text'),
                        'photos': photos
                    })

                return result_feedbacks

            return None


async def fetchProductFeedbacks(nmID):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    URL.product_info.value.format(nmID=nmID),
                    headers=headers) as response:

                text = await response.text()
                data = json.loads(text)
                root = data.get('data').get('products')[0].get('root')

                tasks = [fetchFeedbacksData(feedbacks, root, nmID)
                         for feedbacks
                         in [1, 2]]
                results = await asyncio.gather(*tasks)

                for res in results:
                    if not res is None:
                        return res

                return None
    except:
        return None


async def fetchProductStocks(nmID):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    URL.product_info.value.format(nmID=nmID),
                    headers=headers) as response:

                text = await response.text()
                data = json.loads(text)
                product = data.get('data').get('products')[0]

                return getStocks(product), await fetchWarehouseStocks(product)
    except:
        return None


async def fetchQuery(query, typeQuery):
    if typeQuery == 'normquery':
        url = URL.wildberries_position_autoadvert.value.format(
            query=query, page=1, dest=-1257786)
    elif typeQuery == 'similar_queries':
        url = URL.similar_queries.value.format(query=query)
    else:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url,
                headers=headers) as response:

            if response.status == 200:
                text = await response.text()
                data = json.loads(text)

                if typeQuery == 'normquery':
                    result = data.get('metadata').get('normquery')
                elif typeQuery == 'similar_queries':
                    result = data.get('query')

                return result

            return None


async def fetchSearchQuery(query):
    tasks = [fetchQuery(query, typeQuery)
             for typeQuery
             in ['normquery', 'similar_queries']]
    results = await asyncio.gather(*tasks)

    return results[0], results[1]


async def fetchPartialProductPrice(nmID):
    try:
        result = []
        found = False
        res_prices = {el: [] for el in nmID}
        nmID_data = ';'.join(map(str, nmID))

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    URL.product_info.value.format(nmID=nmID_data),
                    headers=headers) as response:

                text = await response.text()
                data = json.loads(text)
                products = data.get('data').get('products')

                for product in products:
                    res_prices[product.get('id')] = getPrices(product)

                for productID, sizes in res_prices.items():
                    if sizes:
                        found = True

                    result.append({
                        'productID': productID,
                        'sizes': sizes
                    })

                return result, found

    except Exception as e:
        print(e)
        # logging.exception(e)
        return res_prices


async def fetchProductPrice(nmID):
    try:
        nmID = list(set(nmID))
        res_prices = []
        found = False
        tasks = []

        count = 500
        count_step = ceil(len(nmID) / count)

        for cur_500 in range(count_step):
            tasks.append(fetchPartialProductPrice(
                nmID[count*cur_500:count+count*cur_500]))

        results = await asyncio.gather(*tasks)

        for res in results:
            res_prices.extend(res[0])
            if res[1]:
                found = True

        return res_prices, found

    except Exception as e:
        print(e)
        # logging.exception(e)
        return res_prices
