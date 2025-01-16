#https://silviolima07.medium.com/web-scrap-vagas-em-data-science-bc43c7e1be16

#!/usr/bin/env python
#
#from checar_parametros import buscar_campos
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options  as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import pandas as pd
from bs4 import BeautifulSoup
import time
import sys
# Configuracao para não abrir o browse durante execucao
options = FirefoxOptions()
options.add_argument('-headless')
service = Service(r"C:\Program Files (x86)\GeckoDriver\geckodriver.exe")
driver = Firefox(service=service, options=options)
wait = WebDriverWait(driver, timeout=60)
#print ("Headless Firefox Initialized")
# Informacoes de interesse na busca no indeed
cargo=[]
local=[]
empresa=[]
descricao=[]
link_url=[]
#CARGO = 'Analista de dados'
# Em sys.argv recebemos exatamente a linha que foi executada pra iniciar a busca
# sys.argv traz: scrap-indeed.py analista de dados
# O argumento 0 é o nome do script
# Sendo assim pegamos a partir do argumento 1 e definimos o cargo a partir da variavel word
# A variavel word começa vazia e termina valendo: analista de dados
word=''
for i in range(1,len(sys.argv)):
    word=word+sys.argv[i]
    if i != len(sys.argv)-1:
        word=word+' '
# Cargo foi ajustado corretamente
CARGO = word
#print("Pesquisando vagas...")
# Na pagina da indeed por default esta definido que mostrará
# em cada página 10 resultados encontrados
# Nesse caso, começando do 0 a 10, de 10 em 10
# Assim apenas a página inicial será retornada
i=10
driver.get("https://br.indeed.com/empregos?as_ttl=&l=Brasil&sort=date&radius=25&start=" + str(i))
driver.implicitly_wait(50)
# Advanced search
advanced_search = driver.find_element_by_xpath("//a[contains(text(),'Busca Avançada de Vagas')]")
advanced_search.click()
# Enviar na pagina na linha as_ttl, para usar as palavras em CARGO na busca
search_job = driver.find_element_by_xpath('//*[@id="as_ttl"]')
search_job.send_keys([CARGO])
# Apos envio acionar botao para iniciar busca
search_button = driver.find_element_by_xpath('//*[@id="fj"]')
search_button.click()
# Guarda a nova url com o CARGO incluido na busca desejada
url_page = driver.current_url
#url_page = url_page+str('&start=0')
#print("Url com o CARGO pesquisado:", url_page)
# Total de vagas encontradas
# Página 1 de 6,vagas
total_vagas = driver.find_element_by_xpath('//*[@id="searchCountPages"]').text
total_vagas = total_vagas.replace('Página 1 de', '')
total_vagas = total_vagas.replace('vagas', '')
total_vagas = int(total_vagas)
print("\nCargo:", CARGO)
print("Total de vagas:", total_vagas)
    
# Buscar os campos de dados na pagina retorna em all_jobs
cargo, local, empresa, descricao, link_url = buscar_campos(driver, url_page, total_vagas)
driver.quit()
data = {'Cargo': cargo,
        'Local': local,
        'Empresa': empresa,
        'Descrição': descricao,
        'Link' : link_url}
df = pd.DataFrame(data, columns=["Cargo", "Local", "Empresa","Descrição", "Link"])
df_final = df.drop_duplicates()
cargo = CARGO.replace(' ', '_')
print("\nCargo:", cargo)
filename = 'indeed_'+cargo+'.csv'
print("\nCriando arquivo CSV: ", filename)
df_final.to_csv(filename, index=False, header=True)

#!/usr/bin/env python
from url_shortener import make_shorten
#import sys
#import os
from bs4 import BeautifulSoup
##################################################################
    
def buscar_campos(driver, url_page, total_vagas):
    cargo = []
    local = []
    empresa = []
    descricao = []
    link_url = []
    page = 1
    pagina_final = (int(total_vagas / 10) + 1) * 10
    url_page = url_page + str('&start=')
    pagina_limite = 150

    if pagina_final < pagina_limite:
        pagina_limite = pagina_final

    for n in range(0, pagina_limite, 10):
        driver.get(url_page + str(n))
        driver.implicitly_wait(40)
        all_jobs = driver.find_elements_by_class_name('result')

        for job in all_jobs:
            result_html = job.get_attribute('innerHTML')
            soup = BeautifulSoup(result_html, 'html.parser')

            try:
                title = soup.find("a", class_="jobtitle").text.replace('\n', '')
            except:
                title = 'None'
            cargo.append(title)

            try:
                location = soup.find(class_="location").text
            except:
                location = 'None'
            local.append(location)

            try:
                company = soup.find(class_="company").text.replace("\n", "").strip()
            except:
                company = 'None'
            empresa.append(company)

            try:
                summary = soup.find(class_="summary").text.replace("\n", "").strip()
            except:
                summary = 'None'
            descricao.append(summary)

            try:
                indeed = 'https://www.indeed.com'
                link = soup.find("a", class_="jobtitle").attrs['href']
                url = indeed + str(link)
            except:
                url = 'None'
            link_url.append(url)

        page = page + 1

    return (cargo, local, empresa, descricao, link_url)
