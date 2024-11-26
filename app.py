import asyncio
import os

import aiohttp
import pandas as pd

import scrp_func


# 参考URL
# https://moto.webike.net/shop/1009/?dsp=0_50%4051_125&ponly=1&exsld=1&eqp=shinsya&genkosya=0&canonical=true

shop_list = [1009, 1010, 1168, 1229, 1280, 1288, 1289, 1291, 16355, 17972]

if __name__ == "__main__":

    result_save_dir = 'scrape_results'

    if not os.path.exists(result_save_dir):
        os.makedirs(result_save_dir)

    for shop_no in shop_list:
        target_shop_url = f'https://moto.webike.net/shop/{shop_no}/?dsp=0_50%4051_125&ponly=1&exsld=1&eqp=shinsya&genkosya=0&canonical=true'

        bike_detail_url_list = scrp_func.bike_info_url_getter(target_shop_url)

        async def fetch(session, url):
            async with session.get(url) as response:
                return await response.text()

        async def main(url_list):
            async with aiohttp.ClientSession() as session:
                tasks = [fetch(session, url) for url in url_list]
                results = await asyncio.gather(*tasks)
                return results

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(main(bike_detail_url_list))

        bike_data = scrp_func.bike_detail_getter(results, bike_detail_url_list)

        # 辞書型で受け取ったバイクの詳細データをpandasでDataFrame化
        df = pd.DataFrame.from_dict(bike_data)

        # データフレームをCSVで保存
        df.to_csv(
            f'scrape_results/shop_no_{shop_no}_result.csv',
            index=False
        )
