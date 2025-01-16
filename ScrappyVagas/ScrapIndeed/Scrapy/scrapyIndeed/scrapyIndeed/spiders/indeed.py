import scrapy


class IndeedSpider(scrapy.Spider):
    name = "indeed"
    allowed_domains = ["br.indeed.com"]
    start_urls = ['https://br.indeed.com/jobs?q="Trans"&l=Brasil&vjk=32a79d51cbb0d1d7']

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 2  # delay of 2 seconds between requests
    }

    def parse(self, response):
        # Selecionar todos os blocos de vaga
        jobs = response.css('div.job_seen_beacon')
    	
         
        for job in jobs:
            link = job.css("h2 > a::attr(href)").get()
            # Extrair os dados da vaga
            title = job.css('h2 > a::text').get()
        #    company = job.css('span.companyName::text').get()
        #    location = job.css('div.companyLocation::text').get()
        #    salary = job.css('span.salary-snippet::text').get()
        
        # Salvar os dados como um item do Scrapy
        #yield {
        #    'title': title,
        #    'company': company,
        #    'location': location,
        #    'salary': salary,
        #}
    
    # Verificar se há uma próxima página
        #next_page = response.css('a[aria-label="Próxima"]::attr(href)').get()
        #if next_page:
        #    yield response.follow(next_page, callback=self.parse)
        
        pass
