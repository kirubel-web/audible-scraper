from click import option
from matplotlib import container
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import pandas as pd


options = Options()
service = Service()
chrome_driver_path = '/usr/local/bin/chromedriver'


options = webdriver.ChromeOptions()

options.add_experimental_option("detach", True)

# options.add_argument('--headless')

driver = webdriver.Chrome(service=service, options=options)


web = 'https://www.audible.com/adblbestsellers?ref_pageloadid=not_applicable&ref=a_search_t1_navTop_pl0cg1c0r0&pf_rd_p=d42ea6af-6ce9-44e1-bbd5-7e2e15acab17&pf_rd_r=ADWMDAMHHJDYC0SJH401&pageLoadId=sAcPwXMPzLy8w9wC&ref_plink=not_applicable&creativeId=7ba42fdf-1145-4990-b754-d2de428ba482'

driver.get(web)

driver.maximize_window()

# Pagination

pagination = driver.find_element(By.XPATH, '//*[@id="pagination-a11y-skiplink-target"]/div/div[2]/div/span/ul')

pages = pagination.find_elements(By.TAG_NAME, 'li')

last_page = int(pages[-2].text)



book_title = []
book_author = []
book_length = []


current_page = 1

while current_page <= last_page:

    # time.sleep(3) #implict wait

    container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container ')))

    # container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container ')

    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, './div/span/ul/li')))

    # products = container.find_elements(By.XPATH, './div/span/ul/li')


    for product in products:
        book_title.append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        book_author.append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        book_length.append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)

    current_page = current_page + 1
    try:
        next_page = driver.find_element(By.XPATH, "//span[contains(@class, 'nextButton')]")
        next_page.click()
    except:
        pass

df = pd.DataFrame({"Book-Title": book_title, "Book-Author": book_author, "Book-Length": book_length})

df.to_csv('Audible.csv', index=False)

print(df)


