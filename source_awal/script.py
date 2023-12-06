from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from pprint import pprint

import pdb
import time

keywords = input('Masukan kata kunci: ')
url = f'https://www.tokopedia.com/search?st=&q={keywords}&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
driver = webdriver.Chrome()
driver.get(url)

scroll_increment = 100
scroll_duration = 0.3

total_height = int(driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"))
for i in range(0, total_height, scroll_increment):
    driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
    time.sleep(scroll_duration)

soup = BeautifulSoup(driver.page_source, 'html.parser')
elements = soup.find_all('div', class_='css-llwpbs')

id = 1
datas = []
for element in elements:
    # -------------------- Name --------------------
    try:
        name = element.find('div', class_='prd_link-product-name')
        if name:
            name = name.text.strip()
    except:
        name = None
    # -------------------- Image --------------------
    try:
        img = element.find('img', class_='css-1q90pod')
        if img:
            img = img['src']
    except:
        img = None
    # -------------------- Terjual --------------------
    try:
        terjual = element.find('span', class_='prd_label-integrity')
        if terjual:
            terjual = terjual.text.strip()
    except:
        terjual = None
    # -------------------- Rating --------------------
    try:
        rating = element.find('span', class_='prd_rating-average-text')
        if rating:
            rating = rating.text.strip()
    except:
        rating = None
    # -------------------- Link Product --------------------
    try:
        link_product = element.find('a', class_='pcv3__info-content')
        if link_product:
            link_product = link_product.get('href')
    except:
        link_product = None

    datas.append({
        'id': id,
        'name': name,
        'img': img,
        'terjual': terjual,
        'rating': rating,
        'link_product': link_product
    })
    id += 1

for data in datas:
    print(f'---------- Product-{data['id']} ----------')
    pprint(data)
    print('\n')

wait = WebDriverWait(driver, 5)
button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[5]/nav/ul/li[11]/button')))
time.sleep(0.3)
button.location_once_scrolled_into_view
time.sleep(0.3)
driver.execute_script(f"window.scrollBy(0, -250);")
button.click()

stop_program = input('Enter to stop program')