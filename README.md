# Scraping de Vagas

Essa branch realiza o scraping de vagas de emprego direcionadas para pessoas trans usando Selenium e Python. O objetivo é coletar informações detalhadas sobre as vagas e salvá-las em formato JSON.

## Requisitos

Antes de começar, certifique-se de que seu ambiente atende aos seguintes requisitos:

- Python 3.7 ou superior
- Google Chrome instalado
- ChromeDriver compatível com a versão do Google Chrome
- Conexão estável com a internet

## Instalação

1. **Clone o repositório:**

   ```bash
   git clone <url-do-repositorio>
   cd <nome-do-repositorio>
   ```

2. **Abra utilizando o Visual Studio Code ou Similar**

   Abra o projeto em um Visual Studio Code com o python instalado.


3. **Instale as dependências:**

   No terminal do windows, visual studio ou similar execute:
   pip install selenium
   pip install pandas
  
4. **Configure o URL:**

   Certifique-se de que a variável `url` no script aponta para a página correta. Por exemplo:

   ```python
   url = 'https://www.google.com/search?q=vagas+emprego+pessoa+trans'
   ```

5. **Execute o script:**

   No terminal, execute:
 
   python nome_do_arquivo.py
  

6. **Verifique o resultado:**

   Após a execução, o script irá gerar um arquivo JSON com as informações coletadas. O arquivo será salvo no mesmo diretório do script com o nome `vagasGoogle.json`.

## Observações

- Certifique-se de que o Google Chrome esteja instalado e atualizado.
- Dependendo da página, pode ser necessário ajustar os seletores CSS no script.
- Caso o script não funcione como esperado, ative o modo de depuração adicionando prints adicionais ao código ou inspecione o HTML da página para ajustes nos seletores.
# scrapyVagasTCC
