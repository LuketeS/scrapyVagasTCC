import requests
from bs4 import BeautifulSoup
import json

#url vagas em todo Brasil 
url = 'https://www.linkedin.com/jobs/search/?currentJobId=4055468078&geoId=106057199&keywords="trans"&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true'
response = requests.get(url)

# Verifica se a requisição foi bem-sucedida
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lista para armazenar todas as vagas
    job_data = []
    
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
    
    # Salvando os dados no arquivo JSON
    with open('job_listings_Linkedin.json', 'w') as json_file:
        json.dump(job_data, json_file, indent=4)
    
    print(f"Successfully saved {len(job_data)} job listings to job_listings.json")
else:
    print("Failed to fetch job listings.")
