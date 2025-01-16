#https://www.youtube.com/watch?v=_Ri-QjToQ24
#parece que esse requests não funciona em site com javascript

import requests
from bs4 import BeautifulSoup

url = 'https://www.pichau.com.br/hardware/placa-de-video'

headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0"}

site = requests.get(url, headers=headers)
soup = BeautifulSoup(site.content,'html.parser')

vagas = soup.find_all('div', {'class':'MuiCardContent-root jss281'})
#ultima_pagina = soup.find('button', 'MuiButtonBase-root MuiPaginationItem-root MuiPaginationItem-page MuiPaginationItem-textPrimary MuiPaginationItem-sizeLarge')

vaga = vagas[0]
nome = vaga.find('h2', {'class':'MuiTypography-root jss301 jss302 MuiTypography-h6'})

print(nome)