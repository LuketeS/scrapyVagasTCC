#https://www.youtube.com/watch?v=XLkxOBY965w
#find_element(By.ID, "id")
#find_element(By.NAME, "name")
#find_element(By.XPATH, "xpath")
#find_element(By.LINK_TEXT, "link text")
#find_element(By.PARTIAL_LINK_TEXT, "partial link text")
#find_element(By.TAG_NAME, "tag name")
#find_element(By.CLASS_NAME, "class name")
#find_element(By.CSS_SELECTOR, "css selector")

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

url = 'https://books.toscrape.com/'

driver.get(url)

titleElements = driver.find_elements(By.TAG_NAME, 'a')[54:94:2]

titleList = [title.get_attribute('title') for title in titleElements]

stockList = []
#titleElements[0].click()

for title in titleElements:
    print(title.text)
    title.click()    
    qtdStock = driver.find_element(By.CLASS_NAME, 'instock').text
    print(qtdStock)
    stockList.append(qtdStock)
    driver.back()


dictDF = {'title': titleList,
          'stock': stockList}

print(pd.DataFrame(dictDF))

#input("presione enter")
#driver.quit()

