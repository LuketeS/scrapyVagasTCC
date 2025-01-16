import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Configuração do serviço do Chrome
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL do site
url = 'https://www.google.com/search?client=opera-gx&q=vagas%20emprego%20trans%20São%20Paulo,%20SP&sourceid=opera&ie=UTF-8&oe=UTF-8&jbr=sep:0&udm=8&llpgabe=CgkvbS8wMjJwZm0&ved=2ahUKEwjZj6ux7tuJAxU6LLkGHXzJKFsQi5ULKAB6BAgKEAA'
driver.get(url)

# Listas para armazenar dados
titlesList = []
empresaList = []
linksList = []

# Localizar títulos, empresas e links
titles = driver.find_elements(By.CSS_SELECTOR, '.PUpOsf')
empresas = driver.find_elements(By.CSS_SELECTOR, '.a3jPc')
link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.MQUd2b')


# Extraindo os textos dos títulos e empresas
for title in titles:
    titlesList.append(title.text)

for empresa in empresas:     
    empresaList.append(empresa.text)

# Extraindo apenas os links das vagas
for element in link_elements:
    link = element.get_attribute("href")
    linksList.append(link)

# Garantindo que o tamanho das listas seja igual
#min_len = min(len(titlesList), len(empresaList), len(linksList))
#titlesList = titlesList[:min_len]
#empresaList = empresaList[:min_len]
#linksList = linksList[:min_len]

# Criação do DataFrame com os dados
dictDF = {
    'Título': titlesList,
    'Empresa': empresaList,
    'Link': linksList
}

# Convertendo o DataFrame para JSON
df = pd.DataFrame(dictDF)
json_data = df.to_dict(orient="records")  # Convertendo o DataFrame para uma lista de dicionários

# Salvando em um arquivo JSON
with open("vagasGoogle.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)

print("Dados salvos em 'vagasGoogle.json'.")
# Fecha o navegador
driver.quit()
