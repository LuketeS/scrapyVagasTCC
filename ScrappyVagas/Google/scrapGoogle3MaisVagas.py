import pandas as pd
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta

# URL do endpoint para o POST request
post_url = 'http://localhost:8080/empresa/adicionarVagaScraper'

# Configuração do serviço do Chrome
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL do site
url = 'https://www.google.com/search?q=vagas+emprego+pessoa+trans+S%C3%A3o+Paulo%2C+SP&sca_esv=332c1457e26e21ac&rlz=1C1FHFK_pt-PTBR1091BR1091&udm=8&sxsrf=ADLYWIIBuM8hA7UdoL-zqONzmGecH8OQlQ%3A1732276953129&ei=2XJAZ4fFB5PN1sQPz_mG8AQ&ved=0ahUKEwjHlcbD8u-JAxWTppUCHc-8AU4Q4dUDCA8&uact=5&oq=vagas+emprego+pessoa+trans+S%C3%A3o+Paulo%2C+SP&gs_lp=EhVnd3Mtd2l6LW1vZGVsZXNzLWpvYnMiKXZhZ2FzIGVtcHJlZ28gcGVzc29hIHRyYW5zIFPDo28gUGF1bG8sIFNQMggQIRigARjDBDIIECEYoAEYwwQyCBAhGKABGMMESNcNUK0FWKAMcAF4AZABAJgBggGgAc8GqgEDMC43uAEDyAEA-AEBmAIGoALZBMICBxAjGLADGCfCAgoQABiwAxjWBBhHwgIEECMYJ8ICCBAAGIAEGKIEwgIKECEYoAEYwwQYCpgDAIgGAZAGCZIHAzEuNaAH_Sc&sclient=gws-wiz-modeless-jobs&jbr=sep:0'
driver.get(url)

# Rolagem até o final da página para carregar todas as vagas
def scroll_to_bottom(driver, pause_time=2):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pause_time)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print("Rolagem concluída. Todas as vagas carregadas.")

# Listas para armazenar dados
titlesList = []
empresaList = []
linksList = []
locaisList = []
descriptionsList = []
tipoList = []

try:
    scroll_to_bottom(driver)

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.PUpOsf')))
    total_vagas = len(driver.find_elements(By.CSS_SELECTOR, '.PUpOsf'))
    print(f"Total de vagas encontradas: {total_vagas}")

    for index in range(total_vagas):
        try:
            time.sleep(1)
            WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.PUpOsf')))
            titles = driver.find_elements(By.CSS_SELECTOR, '.PUpOsf')
            empresas = driver.find_elements(By.CSS_SELECTOR, '.a3jPc')
            link_elements = driver.find_elements(By.CSS_SELECTOR, 'a.MQUd2b')
            locais = driver.find_elements(By.CSS_SELECTOR, '.wHYlTd.FqK3wc.MKCbgd')
            tipos = driver.find_elements(By.CSS_SELECTOR, '.ApHyTb.ncqQR')

            title_text = titles[index].text if index < len(titles) else "Título não encontrado"
            empresa_text = empresas[index].text if index < len(empresas) else "Empresa não encontrada"
            link_href = link_elements[index].get_attribute("href") if index < len(link_elements) else "Link não encontrado"
            local_text = locais[index].text if index < len(locais) else "Local não encontrado"
            tipo_text = tipos[index].text if index < len(tipos) else "Tipo não encontrado"

            if '\n' in tipo_text:
                tipo_text = tipo_text.split('\n')[-1]

            titlesList.append(title_text)
            empresaList.append(empresa_text)
            linksList.append(link_href)
            locaisList.append(local_text)
            tipoList.append(tipo_text)
            print(f"Vaga {index + 1}: {title_text} - {empresa_text} - {local_text} - {tipo_text}")

            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(titles[index])).click()
            time.sleep(3)  # Aumentar o tempo de espera após clicar
            print(f"Clicando na vaga {index + 1}")

            try:
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span.hkXmid')))
                description = driver.find_element(By.CSS_SELECTOR, 'span.hkXmid').text
                if not description:  # Se a descrição estiver vazia, trate como erro
                    raise Exception("Descrição vazia")
            except Exception as e:
                print(f"Erro ao capturar descrição para a vaga {index + 1}: {e}")
                description = "Descrição não encontrada"
            descriptionsList.append(description)
            print(f"Descrição capturada para a vaga {index + 1}: {description}")

            driver.back()
            time.sleep(2)
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

# Criar o DataFrame
dictDF = {
    'Título': titlesList,
    'nomeEmpresa': empresaList,  # Altere o nome da chave aqui para 'nomeEmpresa'
    'Link': linksList,
    'Descrição': descriptionsList,
    'Local': locaisList,
    'Tipo': tipoList
}

# Converter para DataFrame
df = pd.DataFrame(dictDF)

# Palavras para validação
palavras_chave = ['trans', 'pessoas', 'exclusiva', 'exclusivo', 'oportunidade', 'afirmativa', 'afirmativo']

# Função para contar palavras-chave no título
def conta_palavras_chave(titulo):
    return sum(palavra in titulo.lower() for palavra in palavras_chave)

# Filtrar vagas que contenham pelo menos 2 palavras-chave no título
df_filtrado = df[df['Título'].apply(conta_palavras_chave) >= 2]

# Converter o DataFrame filtrado para lista de dicionários
json_data_filtrado = []
for index, row in df_filtrado.iterrows():
    local_text = row['Local']
    if '•' in local_text:
        local_text = local_text.split('•')[0].strip()
    
    if ',' in local_text:
        cidade, estado = [part.strip() for part in local_text.split(',')]
    else:
        cidade, estado = local_text, "não informado"

    vaga = {
        "titulo": row['Título'],
        "descricao": row['Descrição'],
        "nomeEmpresa": row['nomeEmpresa'],
        "dataInicial": datetime.now().strftime("%Y-%m-%d"),
        "dataFinal": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "link": row['Link'],
        "nivelExperiencia": {"descricao": "não informado"},
        "tipoEmprego": {"descricao": row['Tipo']},
        "tipoModalidade": {"descricao": "Remoto"},
        "endereco": {
            "cidade": cidade,
            "estado": estado
        },
        "categoria": {"descricao": "não informado"}
    }
    json_data_filtrado.append(vaga)

# Salvar em arquivo JSON
try:
    with open("vagasGoogle_filtradas.json", "w", encoding="utf-8") as f:
        json.dump(json_data_filtrado, f, ensure_ascii=False, indent=4)

    print("Dados filtrados salvos em 'vagasGoogle_filtradas.json'.")
except Exception as e:
    print(f"Erro ao salvar os dados filtrados no JSON: {e}")

# Fechar o navegador
driver.quit()



post_url = 'http://localhost:8080/empresa/adicionarVagaScraper'
def truncate_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length]

for vaga in json_data_filtrado:
    vaga['titulo'] = truncate_text(vaga['titulo'], 255)
    vaga['descricao'] = truncate_text(vaga['descricao'], 255)
    vaga['nomeEmpresa'] = truncate_text(vaga['nomeEmpresa'], 255)

# Função para fazer POST de cada vaga no backend
def post_vagas(vagas):
    for vaga in vagas:
        try:
            response = requests.post(post_url, json=vaga)
            if response.status_code == 200:
                print(f"Vaga '{vaga['titulo']}' enviada com sucesso.")
            else:
                print(f"Falha ao enviar a vaga '{vaga['titulo']}': {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Erro ao enviar a vaga '{vaga['titulo']}': {e}")

# Enviar vagas para o backend
post_vagas(json_data_filtrado)