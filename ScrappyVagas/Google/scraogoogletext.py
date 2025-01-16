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


# Configuração do serviço do Chrome
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# URL do site
url = 'https://www.google.com/search?q=vagas+emprego+pessoa+trans+S%C3%A3o+Paulo%2C+SP&sca_esv=332c1457e26e21ac&rlz=1C1FHFK_pt-PTBR1091BR1091&udm=8&sxsrf=ADLYWIIBuM8hA7UdoL-zqONzmGecH8OQlQ%3A1732276953129&ei=2XJAZ4fFB5PN1sQPz_mG8AQ&ved=0ahUKEwjHlcbD8u-JAxWTppUCHc-8AU4Q4dUDCA8&uact=5&oq=vagas+emprego+pessoa+trans+S%C3%A3o+Paulo%2C+SP&gs_lp=EhVnd3Mtd2l6LW1vZGVsZXNzLWpvYnMiKXZhZ2FzIGVtcHJlZ28gcGVzc29hIHRyYW5zIFPDo28gUGF1bG8sIFNQMggQIRigARjDBDIIECEYoAEYwwQyCBAhGKABGMMESNcNUK0FWKAMcAF4AZABAJgBggGgAc8GqgEDMC43uAEDyAEA-AEBmAIGoALZBMICBxAjGLADGCfCAgoQABiwAxjWBBhHwgIEECMYJ8ICCBAAGIAEGKIEwgIKECEYoAEYwwQYCpgDAIgGAZAGCZIHAzEuNaAH_Sc&sclient=gws-wiz-modeless-jobs&jbr=sep:0'
driver.get(url)


