from enum import Enum
import asyncio
import aiohttp
import json


class URL(Enum):
    wildberries_position_autoadvert = 'https://search.wb.ru/exactmatch/ru/common/v5/search?query={query}&resultset=catalog&sort=popular&curr=rub&dest={dest}&page={page}'
    supplier_products = 'https://catalog.wb.ru/sellers/v2/catalog?dest=-1257786&curr=rub&sort=popular&spp={spp}&supplier={supplier}&page={page}'
    product_info = 'https://card.wb.ru/cards/v2/detail?dest=-1257786&curr=rub&nm={nmID}'
    warehouse_name = 'https://static-basket-01.wbbasket.ru/vol0/data/stores-data.json'


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


def getStocks(product):
    try:
        stocks = 0
        for i in product['sizes']:
            for k in i['stocks']:
                stocks += k['qty']
        return stocks
    except:
        return 0


async def getWarehouseStocks(product):
    try:
        async with aiohttp.ClientSession() as client:
            async with client.get(URL.warehouse_name.value) as response:
                warehouse_data = await response.json()
                warehouse_name = {warehouse.get('id'): warehouse.get('name')
                                  for warehouse
                                  in warehouse_data}

                stocks = {}
                for i in product['sizes']:
                    for k in i['stocks']:
                        if k['wh'] not in stocks:
                            stocks[k['wh']] = {
                                'name': warehouse_name.get(k.get('wh')),
                                'totalStocks': 0,
                                'data': {}
                            }

                        size_name = i.get('name') if i.get(
                            'name') else 'noneName'
                        orig_name = i.get('origName') if i.get(
                            'name') else 'noneName'

                        stocks[k['wh']]['data'][size_name] = {
                            'origName': orig_name,
                            'stocks': k['qty']
                        }
                        stocks[k['wh']]['totalStocks'] += k['qty']

                return stocks
    except:
        return {}


async def fetchPageSupplierProducts(supplier, page):
    res_products = {}
    product_id = []

    print(page)
    async with aiohttp.ClientSession() as session:
        async with session.get(
                URL.supplier_products.value.format(
                spp=0, supplier=supplier, page=page),
                headers=headers) as response:

            text = await response.text()
            data = json.loads(text)
            products = data.get('data').get('products')

            if products == []:
                return None

            for product in products:
                colors = [color.get('name')
                          for color in product.get('colors')]
                salePriceU = product.get('sizes')[0].get(
                    'price').get('total') // 100
                salePrice = product.get('sizes')[0].get(
                    'price').get('basic') // 100

                res_products[product.get('id')] = {
                    'name': product.get('name'),
                    'salePriceU': salePriceU,
                    'salePrice': salePrice,
                    'colors': colors
                }
                product_id.append(product.get('id'))

            return res_products, product_id


async def fetchSupplierProducts(supplier):
    res_products = {}
    start_page = 1
    check_count_page = 5
    count_attempts = 1

    while True:
        product_id = []

        while True:
            end_find = False
            tasks = [fetchPageSupplierProducts(supplier, page)
                     for page
                     in range(start_page, start_page+check_count_page)]
            results = await asyncio.gather(*tasks)

            for res in results:
                if res is None:
                    end_find = True
                    break

                res_products.update(res[0])
                product_id.extend(res[1])

            if end_find:
                break
            start_page += check_count_page

        if count_attempts == 10:
            print(f'{count_attempts} attempts ERROR')
            return None

        if len(res_products) != len(product_id):
            count_attempts += 1

        break

    return res_products


async def fetchSupplierProductsAAAAA(supplier):
    res_products = {}
    count_attempts = 1

    while True:
        page = 1
        product_id = []
        try:
            while True:
                print(page)

                async with aiohttp.ClientSession() as session:
                    async with session.get(
                            URL.supplier_products.value.format(
                            spp=0, supplier=supplier, page=page),
                            headers=headers) as response:

                        text = await response.text()
                        data = json.loads(text)
                        products = data.get('data').get('products')

                        if products == []:
                            break

                        for product in products:
                            colors = [color.get('name')
                                      for color in product.get('colors')]
                            salePriceU = product.get('sizes')[0].get(
                                'price').get('total') // 100
                            salePrice = product.get('sizes')[0].get(
                                'price').get('basic') // 100

                            res_products[product.get('id')] = {
                                'name': product.get('name'),
                                'salePriceU': salePriceU,
                                'salePrice': salePrice,
                                'colors': colors
                            }
                            product_id.append(product.get('id'))

                        page += 1
        except:
            count_attempts += 1

            if count_attempts == 10:
                print(f'{count_attempts} attempts ERROR')
                # logging.error(f'{count_attempts} attempts ERROR')
                return {}

            await asyncio.sleep(0.1)
            continue

        if len(res_products) == len(product_id):
            print(f'{supplier} get_products success')
            # logging.info(f'{supplier} get_products success')
            break

        if count_attempts == 10:
            print(f'{count_attempts} attempts ERROR')
            # logging.error(f'{count_attempts} attempts ERROR')
            return {}

        count_attempts += 1
        await asyncio.sleep(0.1)

    return res_products


async def fetchPositionAutoadvertProduct(query, dest, page, suppliers):
    try:
        res_position_advert = {supplier: {} for supplier in suppliers}
        res_position_total = {supplier: {} for supplier in suppliers}

        flag_foud = False
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
                                    if (product_id not in res_position_total.get(supplierId)
                                            or pagePosition < res_position_total.get(supplierId).get(product_id).get('pagePosition')):
                                        res_position_total[supplierId][product_id] = {
                                            'active': False,
                                            'advertPosition': None,
                                            'pagePosition': 100 * (page - 1) + pagePosition
                                        }

                                if el.get('log'):
                                    autoadvert.append(
                                        (
                                            product_id,
                                            el.get('log').get(
                                                'promoPosition') + 1,
                                            supplierId
                                        )
                                    )

                        except Exception as e:
                            print(e)
                            # logging.exception(e)

                        for advertPosition, advert in enumerate(autoadvert, 1):
                            try:
                                supplierId = advert[-1]
                                if supplierId not in suppliers:
                                    continue

                                flag_foud = True
                                product_id = advert[0]
                                pagePosition = advert[1]

                                if (product_id not in res_position_advert.get(supplierId)
                                        or pagePosition < res_position_advert.get(supplierId).get(product_id).get('pagePosition')):
                                    res_position_advert[supplierId][product_id] = {
                                        'active': True,
                                        'advertPosition': advertPosition,
                                        'pagePosition': pagePosition
                                    }

                                if product_id in res_position_total.get(supplierId):
                                    res_position_total[supplierId][product_id]['active'] = True
                                    res_position_total[supplierId][product_id]['advertPosition'] = advertPosition

                            except Exception as e:
                                print(e)
                                # logging.exception(e)
                        break

                    await asyncio.sleep(0.1)

        return res_position_advert, res_position_total

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


async def fetchFindProductPosition(query, nmID, dest):
    try:
        tasks = [fetchFindPageProduct(query, nmID, dest, page)
                 for page
                 in range(1, 6)]
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
    async with aiohttp.ClientSession() as session:
        async with session.get(
                URL.product_info.value.format(nmID=nmID),
                headers=headers) as response:

            try:
                text = await response.text()
                data = json.loads(text)

                pics_amount = data.get('data').get('products')[0].get('pics')
                part = nmID // 1000
                vol = part // 100
                basket = getBasket(vol)

                return [f'https://basket-{basket}.wbbasket.ru/vol{vol}/part{part}/{nmID}/images/big/{pics_number}.jpg'
                        for pics_number
                        in range(1, pics_amount+1)]
            except:
                return None


async def fetchProductStocks(nmID):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                URL.product_info.value.format(nmID=nmID),
                headers=headers) as response:

            try:
                data = await response.json()
                product = data.get('data').get('products')[0]

                return getStocks(product), await getWarehouseStocks(product)
            except:
                return None
