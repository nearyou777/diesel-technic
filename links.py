import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import undetected_chromedriver as uc
from time import sleep
from threading import Thread
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
cookies = {
    'node': 'd31ac89d8c759f4e',
    'sid_key': 'oxid',
    'logged_in': 'no',
    '__cmpconsentx58190': 'BP12j_7P12j_7AfC-BRUABAAAAAAAA',
    '__cmpcccx58190': 'aBP12j_7gAwAzADQAgAAIAFwANAAeAEOA4kCDIF5AAU16g',
    '_gid': 'GA1.2.2035517456.1700962305',
    'browserLanguageCookie': 'RU',
    'language': '0',
    'sid': '3vdmmgaj98bicjhj2mum9o5f0j',
    '_gat_UA-7557542-18': '1',
    '_ga': 'GA1.1.687034203.1700962305',
    '_ga_M0GSMWFZLE': 'GS1.1.1701021631.3.1.1701021649.0.0.0',
}

headers = {
    'authority': 'partnerportal.dieseltechnic.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'node=d31ac89d8c759f4e; sid_key=oxid; logged_in=no; __cmpconsentx58190=BP12j_7P12j_7AfC-BRUABAAAAAAAA; __cmpcccx58190=aBP12j_7gAwAzADQAgAAIAFwANAAeAEOA4kCDIF5AAU16g; _gid=GA1.2.2035517456.1700962305; browserLanguageCookie=RU; language=0; sid=3vdmmgaj98bicjhj2mum9o5f0j; _gat_UA-7557542-18=1; _ga=GA1.1.687034203.1700962305; _ga_M0GSMWFZLE=GS1.1.1701021631.3.1.1701021649.0.0.0',
    'referer': 'https://partnerportal.dieseltechnic.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

res = []

def get_links(n_links:str):
    for url in n_links:
        response = requests.get(
            url,
            cookies=cookies,
            headers=headers,
        )
        print(response)
        soup = BeautifulSoup(response.text, 'lxml')
        for item in soup.find_all('div', class_='nxsArticleRowContainer'):
            res.append(item.find('a').get('href'))




def main():
    with open('categories.json', 'r') as f:
        links = json.load(f)
    links = list(dict.fromkeys(links.split()))
    num_threads = 16
    print(len(links))
    threads = []
    batch_size  = len(links) // num_threads
    for i in range(num_threads):
        start = i * batch_size
        end = start + batch_size if num_threads -1 else len(links)
        t =  Thread(target=get_links, args=(links[start:end], ))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    with open('links.json', 'r') as f:
        res = list(dict.fromkeys(json.load(f)))
    with open('links.json', 'w') as f:
        json.dump(res,f,indent=2)

if __name__ == '__main__':
    main()
