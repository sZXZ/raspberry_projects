import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd


def _get_args():
    parser = argparse.ArgumentParser(description='Saves pages content to csv')
    parser.add_argument('-s', '--site', default='https://www.google.com/')
    parser.add_argument('-t', '--tags', default=['input'])
    parser.add_argument('-c', '--csv', default='output.csv')
    return vars(parser.parse_args())


def do(csv, tags, site, use_class_filter=False, class_filter=''):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome("/Applications/chromedriver", options=chrome_options)
    try:
        driver.get(site)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        data_dict = {}
        data_array = []
        for tag in tags:
            if use_class_filter:
                data = soup.findAll(tag, attrs={'class': class_filter})
            else:
                data = soup.findAll(tag)
            for data_part in data:
                data_array.append(data_part.text)
            data_dict[tag+class_filter] = data_array
        df = pd.DataFrame(data_dict)
        df.to_csv(csv, index=False, encoding='utf-8')
        driver.quit()
        return df
    except:
        driver.quit()


if __name__ == "__main__":
    do(**_get_args())
