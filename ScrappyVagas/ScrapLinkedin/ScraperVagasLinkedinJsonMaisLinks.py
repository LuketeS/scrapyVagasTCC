import requests
from bs4 import BeautifulSoup
import json

# URLs para busca de vagas
urls = [
    'https://www.linkedin.com/jobs/search/?currentJobId=4055468078&geoId=106057199&keywords="trans"&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true',
    'https://www.linkedin.com/jobs/search/?currentJobId=4065630146&geoId=106057199&keywords="trans"%20-transporte&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true&start=25'
    'https://www.linkedin.com/jobs/search/?currentJobId=4057935037&geoId=106057199&keywords="trans"%20-transporte&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true&start=50'
    'https://www.linkedin.com/jobs/search/?currentJobId=4065625715&geoId=106057199&keywords="trans"%20-transporte&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true&start=75'
    'https://www.linkedin.com/jobs/search/?currentJobId=4065627450&geoId=106057199&keywords="trans"%20-transporte&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&spellCorrectionEnabled=true&start=100' 
]

# Lista para armazenar todas as vagas
job_data = []

# Itera sobre cada URL
for url in urls:
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra todas as vagas na página
        job_listings = soup.find_all('div', {'class': 'job-search-card'})
        
        for job in job_listings:
            # Extraindo informações de cada vaga
            title = job.find('h3', {'class': 'base-search-card__title'}).text.strip()
            company = job.find('a', {'class': 'hidden-nested-link'}).text.strip()
            location = job.find('span', {'class': 'job-search-card__location'}).text.strip()
            anchor_tag = job.find('a', class_='base-card__full-link')
            href_link = anchor_tag['href']
            
            # Adicionando os dados da vaga em um dicionário
            job_info = {
                'title': title,
                'company': company,
                'location': location,
                'link': href_link
            }
            
            # Adiciona o dicionário à lista de vagas
            job_data.append(job_info)
    
    else:
        print(f"Failed to fetch job listings from {url}")

# Salvando os dados no arquivo JSON
with open('Vagas Linkedin.json', 'w') as json_file:
    json.dump(job_data, json_file, indent=4)

print(f"Successfully saved {len(job_data)} job listings to job_listings_Linkedin.json")
