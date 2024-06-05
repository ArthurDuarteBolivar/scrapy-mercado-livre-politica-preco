from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from mercadolivre.spiders.ml import MlSpider
from scrapy import signals
from twisted.internet import reactor

options = ["Storm 40", "Storm 60", "Lite 60", "Storm 70", "Lite 70", "Bob 90", "Storm 120", "Lite 120", "Bob 120", "Storm 200", "Storm 200 MONO", "Bob 200", "Lite 200"]

settings = get_project_settings()

process = CrawlerProcess(settings)

# Função a ser chamada quando o spider terminar
def spider_closed(spider):
    print(f'Spider {spider.name} has finished scraping.')
    # Aqui você pode adicionar qualquer ação que deseja realizar após o término do spider
    reactor.stop()  # Parar o reactor

# Conectar a função ao sinal spider_closed
for spider_name in options:
    crawler = process.create_crawler(MlSpider)
    crawler.signals.connect(spider_closed, signal=signals.spider_closed)
    process.crawl(crawler, palavra=spider_name)

# Iniciar o processo de scraping
process.start()
