import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuração do driver
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")  # Abre a janela maximizada para parecer mais natural
driver = webdriver.Chrome(options=options)

# URL do site
url = 'https://portal.gupy.io/job-search/term=trans'
driver.get(url)

# Esperar que a página carregue completamente
wait = WebDriverWait(driver, 10)

# Listas para armazenar dados
titlesList = []
empresaList = []
linksList = []

# Função para rolar a página até o fim
def scroll_down_page(driver, pause_time=1.5, max_scroll=10):
    """Rola a página até o final lentamente para carregar as vagas"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    scroll_count = 0
    while scroll_count < max_scroll:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)  # Pausa para permitir o carregamento dos dados dinamicamente
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:  # Verifica se chegou ao final da página
            break
        last_height = new_height
        scroll_count += 1

# Rolar a página e carregar vagas adicionais
scroll_down_page(driver)

# Coleta os dados após o carregamento completo
try:
    # Espera explícita para garantir que os elementos estejam presentes
    titles = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sc-evZas.bdbCHA.sc-4d881605-2.evSPWd')))
    empresas = driver.find_elements(By.CSS_SELECTOR, '.empresa-classe-css')  # Ajuste o seletor para o campo de empresa, se necessário
    link_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="linkElement"]')

    # Extraindo os textos dos títulos
    for title in titles:
        titlesList.append(title.text)

    # Extraindo os textos das empresas (se o seletor for encontrado corretamente)
    for empresa in empresas:
        empresaList.append(empresa.text)

    # Extraindo apenas os links das vagas
    for element in link_elements:
        link = element.get_attribute("href")
        if "/o/" in link:  # Filtrando apenas links que contenham "/o/"
            linksList.append(link)

except Exception as e:
    print(f"Ocorreu um erro ao coletar dados: {e}")

# Verifica se algum dado foi coletado
if not titlesList:
    print("Nenhum título de vaga encontrado. Verifique os seletores ou a lógica de carregamento da página.")
else:
    print(f"Coletados {len(titlesList)} títulos de vaga.")

# Garantindo que o tamanho das listas seja igual
min_len = min(len(titlesList), len(empresaList), len(linksList))
titlesList = titlesList[:min_len]
empresaList = empresaList[:min_len]
linksList = linksList[:min_len]

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
if json_data:
    with open("vagasGupy.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print("Dados salvos em 'vagasGupy.json'.")
else:
    print("Nenhum dado para salvar. Verifique a coleta de informações.")

# Fecha o navegador
driver.quit()
