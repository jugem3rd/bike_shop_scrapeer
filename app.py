import asyncio

import aiohttp
import pandas as pd

import scrp_func

# target_url = 'https://moto.webike.net/shop/1009/?dsp=0_50%4051_125&ponly=1&exsld=1&eqp=shinsya&genkosya=0&canonical=true'
shop_list = [1009, 1010, 1168, 1229, 1280, 1288, 1289, 1291, 16355, 17972]

if __name__ == "__main__":
    url_list = []
    for shop_no in shop_list:
        shop_url = f'https://moto.webike.net/shop/{shop_no}/?dsp=0_50%4051_125&ponly=1&exsld=1&eqp=shinsya&genkosya=0&canonical=true'
        url_list.append(shop_url)
    #url_list = scrp_func.bike_info_url_getter(target_url)

    async def fetch(session, url):
        async with session.get(url) as response:
            return await response.text()


    async def main(url_list):
        async with aiohttp.ClientSession() as session:
            tasks = [fetch(session, url) for url in url_list]
            results = await asyncio.gather(*tasks)
            return results


    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(main(url_list))

    bike_data = scrp_func.bike_detail_getter(results, url_list)

    df = pd.DataFrame.from_dict(bike_data)

    print(df)