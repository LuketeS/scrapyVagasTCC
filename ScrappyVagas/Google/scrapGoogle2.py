import pandas as pd
import json
import time
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
url = 'https://www.google.com/search?q=vagas%20emprego%20trans&rlz=1C1FHFK_pt-PTBR1091BR1091&oq=vagas%20em&gs_lcrp=EgZjaHJvbWUqCAgAEEUYJxg7MggIABBFGCcYOzIICAEQRRgnGDsyBggCEEUYOTIKCAMQABiSAxiABDINCAQQABiSAxiABBiKBTIVCAUQABhDGIMBGLEDGMkDGIAEGIoFMgcIBhAAGIAEMgcIBxAAGIAEMgoICBAAGLEDGIAEMgcICRAAGIAE0gEIMTYzNWowajeoAgCwAgA&sourceid=chrome&ie=UTF-8&jbr=sep:0&udm=8&ved=2ahUKEwj1_qqo9O2JAxV_Q7gEHfUZHEYQ3L8LegQIJBAN'
driver.get(url)

# Listas para armazenar dados
titlesList = []
empresaList = []
linksList = []
locaisList = []
descriptionsList = []

try:
    # Localizar títulos e empresas na página inicial
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.PUpOsf')))
    total_vagas = len(driver.find_elements(By.CSS_SELECTOR, '.PUpOsf'))
    print(f"Total de vagas encontradas: {total_vagas}")

    # Processar cada vaga
    for index in range(total_vagas):
        try:
            # Recarregar os elementos da lista
            time.sleep(1)  # Delay explícito para evitar problemas de carregamento
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.PUpOsf')))
            titles = driver.find_elements(By.CSS_SELECTOR, '.PUpOsf')
            empresas = driver.find_elements(By.CSS_SELECTOR, '.a3jPc')
            link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.MQUd2b')
            locais = driver.find_elements(By.CSS_SELECTOR, '.wHYlTd.FqK3wc.MKCbgd')

            # Obter título, empresa e link da vaga
            title_text = titles[index].text if index < len(titles) else "Título não encontrado"
            empresa_text = empresas[index].text if index < len(empresas) else "Empresa não encontrada"
            link_href = link_elements[index].get_attribute("href") if index < len(link_elements) else "Link não encontrado"
            local_text = locais[index].text if index < len(locais) else "Título não encontrado"

            titlesList.append(title_text)
            empresaList.append(empresa_text)
            linksList.append(link_href)
            locaisList.append(local_text)
            print(f"Vaga {index + 1}: {title_text} - {empresa_text} - {local_text}")

            # Clicar no título da vaga
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(titles[index])).click()
            time.sleep(2)  # Tempo para garantir que a página carregue completamente
            print(f"Clicando na vaga {index + 1}")

            # Aguardar e capturar a descrição via span com a classe hkXmid
            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hkXmid')))
                description = driver.find_element(By.CSS_SELECTOR, 'span.hkXmid').text
            except Exception as e:
                print(f"Erro ao capturar descrição para a vaga {index + 1}: {e}")
                description = "Descrição não encontrada"
            descriptionsList.append(description)
            print(f"Descrição capturada para a vaga {index + 1}")

            # Retornar à página anterior
            driver.back()
            time.sleep(2)  # Tempo para garantir que a página principal recarregue completamente
            print(f"Retornando à página principal para a vaga {index + 1}")

        except Exception as e:
            print(f"Erro ao processar a vaga {index + 1}: {e}")
            descriptionsList.append("Erro ao obter descrição")
            continue
except Exception as e:
    print(f"Erro geral no scraping: {e}")

# Garantir tamanho igual das listas
min_len = min(len(titlesList), len(empresaList), len(linksList), len(descriptionsList))
titlesList = titlesList[:min_len]
empresaList = empresaList[:min_len]
linksList = linksList[:min_len]
descriptionsList = descriptionsList[:min_len]

# Criar o DataFrame e salvar em JSON
dictDF = {
    'Título': titlesList,
    'Empresa': empresaList,
    'Link': linksList,
    'Descrição': descriptionsList,
    'Local' : locaisList
}

try:
    df = pd.DataFrame(dictDF)
    json_data = df.to_dict(orient="records")  # Convertendo o DataFrame para lista de dicionários

    # Salvar em arquivo JSON
    with open("vagasGoogle.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print("Dados salvos em 'vagasGoogle.json'.")
except Exception as e:
    print(f"Erro ao salvar os dados no JSON: {e}")

# Fechar o navegador
driver.quit()
