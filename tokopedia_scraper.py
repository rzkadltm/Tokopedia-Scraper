from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from pprint import pprint

import pdb
import time
import csv

class TokopediaScraper:
    def __init__(self):
        self.datas = []
        self.id = 1
        self.driver = webdriver.Chrome()
        self.base_url = 'https://www.tokopedia.com/search?st=&q='
        self.page_url = '&srp_component_id=02.01.00.00&srp_page_id=&srp_page_title=&navsource='
        self.scroll_increment = 100
        self.scroll_duration = 0.3
    
    def run(self, keywords, pages):
        for _ in range(pages):
            url = f'{self.base_url}{keywords}{self.page_url}'
            self.driver.get(url)
            total_height = int(self.driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight );"))
            for i in range(0, total_height, self.scroll_increment):
                self.driver.execute_script(f"window.scrollBy(0, {self.scroll_increment});")
                time.sleep(self.scroll_duration)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            elements = soup.find_all('div', class_='css-llwpbs')

            for element in elements:
                # -------------------- Name --------------------
                try:
                    nama_product = element.find('div', class_='prd_link-product-name')
                    if nama_product:
                        nama_product = nama_product.text.strip()
                except:
                    nama_product = None
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
                # -------------------- Lokasi --------------------
                try:
                    lokasi = element.find('span', class_='prd_link-shop-loc')
                    if lokasi:
                        lokasi = lokasi.text.strip()
                except:
                    lokasi = None
                # -------------------- Nama Toko --------------------
                try:
                    nama_toko = element.find('span', class_='prd_link-shop-name')
                    if nama_toko:
                        nama_toko = nama_toko.text.strip()
                except:
                    nama_toko = None
                    
                self.datas.append({
                    'id': self.id,
                    'nama_product': nama_product,
                    'img': img,
                    'terjual': terjual,
                    'rating': rating,
                    'link_product': link_product,
                    'lokasi': lokasi,
                    'nama_toko': nama_toko
                })
                self.id += 1
        
            for data in self.datas:
                print(f'---------- Product-{data['id']} ----------')
                pprint(data)
                print('\n')
            
            wait = WebDriverWait(self.driver, 5)
            button = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[2]/div[5]/nav/ul/li[11]/button')))
            time.sleep(0.3)
            button.location_once_scrolled_into_view
            time.sleep(0.3)
            self.driver.execute_script(f"window.scrollBy(0, -250);")
            button.click()

        for row in self.datas:
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = value.replace('|', ',')
        
        csv_file_name = f'data_{keywords}_tokopedia.csv'
        field_names = ["id", "nama_product", "terjual", "rating", "lokasi", "nama_toko", "img", "link_product"]
        with open(csv_file_name, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names, delimiter='|')
            writer.writeheader()
            writer.writerows(self.datas)
        
        stop_program = input('Enter to stop program')