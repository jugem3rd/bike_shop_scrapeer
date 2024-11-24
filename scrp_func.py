from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def bike_info_url_getter(target_url):
    driver = webdriver.Chrome()
    driver.get(target_url)

    sleep(2)
    # 現在のウィンドウの高さを取得
    winHeight = driver.execute_script("return window.innerHeight")

    # スクロール開始位置の初期化
    lastTop = 1

    # 無限スクロールページの最下部までループ
    while True:
        # スクロール前のページの高さを取得
        lastHeight = driver.execute_script("return document.body.scrollHeight")

        # スクロールの開始位置を設定
        top = lastTop

        # 最下部まで徐々にスクロールする
        while top < lastHeight:
            top += int(winHeight * 0.8)
            driver.execute_script("window.scrollTo(0, %d)" % top)
            sleep(0.1)

        # スクロール後のページの高さを取得
        sleep(1)
        newLastHeight = driver.execute_script("return document.body.scrollHeight")

        # スクロール前後で高さに変化がなくなったら終了
        if lastHeight == newLastHeight:
            break

        # ループが終了しなければ現在の高さを再設定して次のループ
        lastTop = lastHeight

    bike_url_list = []

    elems = driver.find_elements(By.CLASS_NAME, 'li_bike_list.jyoukyo1.v2')

    for elem in elems:
        url_obj = elem.find_element(By.CLASS_NAME, 'flex')
        url = url_obj.get_attribute('href')
        bike_url_list.append(url)

    return bike_url_list

def bike_detail_getter(aiohttp_results, url_list):
    price_list = []
    maker_list = []
    model_list = []
    displacement_list = []

    for result in aiohttp_results:
        soup = BeautifulSoup(result, "html.parser")

        # 価格を取得
        price_tag = soup.find('p', string='本体価格').find_next().find_next()
        price_value = price_tag.text
        price_list.append(price_value)

        # メーカー名を取得
        maker_tag = soup.find('th', string='メーカー').find_next()
        maker_value = maker_tag.text
        maker_list.append(maker_value)

        # モデル名を取得
        model_tag = soup.find('th', string='モデル名').find_next()
        model_value = model_tag.text
        model_list.append(model_value)

        # 排気量を取得
        displacement_tag = soup.find('th', string='排気量').find_next()
        displacement_value = displacement_tag.text
        displacement_list.append(displacement_value)

    bike_data = {'価格': price_list,
                 'メーカー': maker_list,
                 'モデル名': model_list,
                 '排気量': displacement_list,
                 '掲載ページ': url_list}

    return bike_data

