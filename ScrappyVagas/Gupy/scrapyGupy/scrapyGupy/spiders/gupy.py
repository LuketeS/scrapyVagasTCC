import scrapy


class GupySpider(scrapy.Spider):
    name = "gupy"
    #allowed_domains = ["portal.gupy.io"]
    start_urls = ["https://portal.gupy.io/job-search/term=trans"]

    def parse(self, response):

        jobs = response.css('div.evSPWd')        

        for job in jobs:
        # Extrair os dados da vaga
            title = job.css('h3 a::text').get()
            #.dZRYPZ
            company = job.css('span.companyName::text').get()
            #.bpsGtj
            location = job.css('div.companyLocation::text').get()
            #.cezNaf
        
        # Salvar os dados como um item do Scrapy
            yield {
                'title': title,
                'company': company,
                'location': location,
        }     












        pass
