#https://www.youtube.com/watch?v=PPcgtx0sI2E
#eu e outras pessoas estamos recebendo o erro 403, parece que Indeed está bloqueando o acesso
import requests
from bs4 import BeautifulSoup

def extract(page):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0'}
    url = f'https://br.indeed.com/jobs?q=python&l=São+Paulo%2C+SP&start={page}&vjk=afffc8e8c0ff01c0'
    r = requests.get(url, headers)
    return r.status_code

print(extract(0))