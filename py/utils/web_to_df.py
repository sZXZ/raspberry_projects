from bs4 import BeautifulSoup
import pandas as pd
import requests

def get_table(url, use_class_filter=False, class_filter='') -> pd.DataFrame:
    '''Finds all table tag on html page and creates DataFrame
    You can grab page with requests.get().contnent
    Class filter lets you select tables by specific class found in the table tag
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, features="html.parser")
    if use_class_filter:
        tables = soup.findAll('table', attrs={'class': class_filter})
    else:
        tables = soup.findAll('table')
    df = pd.read_html(str(tables))
    return df

def get_soup(url) -> pd.DataFrame:
    '''get website
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, features="html.parser")
    return soup
