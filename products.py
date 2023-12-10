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
def get_data(links:list):
    driver = uc.Chrome()
    driver.maximize_window()
    for idx, url in enumerate(links):
        # r =requests.get(url, headers=headers, cookies=cookies)

        driver.get(url)
        sleep(0.07)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        product_detail_span = soup.select_one('.product-detail__section-title')
        product_detail = product_detail_span.text.strip() if product_detail_span else ""
        try:
            categories = '->'.join([i.text.strip() for i in soup.find('ul', class_='breadcrumbs__list').find_all('li')[2:-1]])
        except:
            sleep(2)
            try:
                categories = '->'.join([i.text.strip() for i in soup.find('ul', class_='breadcrumbs__list').find_all('li')[2:-1]])
            except:
                driver.get('https://partnerportal.dieseltechnic.com/en/Mounting-kit-clutch-131353.html')
                sleep(2)
                srch = driver.find_element(by.XPATH, '//*[@id="search_text"]')
                srch.send_keys(url.split('-')[-1].replace('.html', ''))
                sleep(1)
                soup = BeautifulSoup(driver.page_source, 'lxml')
                try:
                    driver.get(soup.find('ul', id='suggest_main').find('a').get('href'))
                    sleep(0.5)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    categories = '->'.join([i.text.strip() for i in soup.find('ul', class_='breadcrumbs__list').find_all('li')[2:-1]])
                except:
                    driver.get(url)
                    sleep(0.5)
                    soup = BeautifulSoup(driver.page_source, 'lxml')
                    try:
                        categories = '->'.join([i.text.strip() for i in soup.find('ul', class_='breadcrumbs__list').find_all('li')[2:-1]])
                    except:
                        print('asfdasrfdsfads')
                        continue
        category = soup.find('ul', class_='breadcrumbs__list').find_all('li')[2].text.strip()
        subcategory = soup.find('ul', class_='breadcrumbs__list').find_all('li')[-2].text.strip()
        subcategory2 = soup.find('ul', class_='breadcrumbs__list').find_all('li')[-3].text.strip()

        # Fetching product detail
        product_name = soup.h1.contents[-1].strip()
        gtin = None
        for i in soup.find('div',id='nxsZoomContainer').find_all('div', class_='row'):
            
            if 'GTIN' in i.find('div').text.strip():
                gtin = i.find_all('div')[-1].text.strip()

            if 'suitable for' in i.find('div').text.strip():
                suit = i.find_all('div')[-1].text.strip()

            if 'PU weight' in i.find('div').text.strip():
                pack_unit = i.find_all('div')[-1].find('p').text.strip()

                pack_weight = i.find_all('div')[-1].find_all('p')[-1].text.strip()
        replaces = []
        ref_num = []
        properties = []
        s_d = []
        data = []
        for row in soup.find('table', class_='row details-table__table details-table__table--produktdetails display').find('tbody').find_all('tr'):
            replaces.append(row.find_all('td')[0].text.strip())
            ref_num.append(row.find_all('td')[1].text.strip())
            properties.append(row.find_all('td')[2].text.strip())
            s_d.append(row.find_all('td')[3].text.strip())
            data.append(row.find_all('td')[4].text.strip())
        doc_name = []
        doc_link = []
        try:
            for row in soup.find('table', class_='row details-table__table details-table__table--media display').find('tbody').find_all('tr'):
                doc_name.append(row.find_all('td')[0].text.strip())
                doc_link.append(row.find_all('td')[1].find('a').get('href'))
        except:
            doc_name = ['']
            doc_link = ['']
        vech_brand = []
        info = []
        try:
            for row in soup.find('table', class_='row details-table__table details-table__table--kompakt display').find('tbody').find_all('tr'):
                vech_brand.append(row.find_all('td')[0].text.strip())
                info.append(row.find_all('td')[1].text.strip())
        except:
            vech_brand = ['']
            info = ['']
        try:
            images = [i.get('src') for i in soup.find('div', role='listbox').find_all('img')]
        except:
            print(url)
            continue
        image_names = []
        for id, i in enumerate(images):
            with open(fr'imgs\{product_name.replace(" ","_").replace(r"/","_")}{idx}_{id}.jpg', 'wb') as f:
                try:
                    img_data = requests.get(i, headers=headers)
                except:
                    images.pop(id)
                    continue
                f.write(img_data.content)
            image_names.append(fr'imgs\{product_name.replace(" ","_")}{idx}_{id}.jpg')
        res.append([url,product_detail, product_name,category,subcategory,subcategory2, gtin, suit, pack_unit,pack_weight, '\n'.join(replaces), '\n'.join(ref_num),'\n'.join(properties), '\n'.join(s_d), '\n'.join(data), '\n'.join(doc_name), '\n'.join(doc_link), '\n'.join(vech_brand),'\n'.join(info), '\n'.join(image_names), '\n'.join(images), categories])
def save(data):        
    cols = ['Link','Product Detail', 'Product Name','Category','SubCategory','SubCategory' ,'Gtin', 'suitable for', 'Packaging Unit','Packaging Weight', 'Replaces', 'Ref. No.', 'Properties', ' ', 'Data', 'Documents', 'Media', 'Vehicle brand','Model, Engine, Gearbox, Axle, Cabin','Images_Path', 'Images Links', 'All categories']
    df = pd.DataFrame(data=data, columns=cols)
    df.to_csv('filename.csv', index=False, encoding='utf-8')



def main():
    with open('links.json', 'r') as f:
        links=  json.load(f)
    
    num_threads = 4
    batch_size = len(links) // num_threads
    threads = []
    for i in range(num_threads):
        start = i * batch_size
        end = start + batch_size if i < num_threads -1 else len(links)
        t = Thread(target=get_data, args=(links[start:end], ))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

    save(res)


if __name__ == '__main__':
    main()