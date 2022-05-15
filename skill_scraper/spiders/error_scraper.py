from scrapy import Spider, signals
from pandas import *

class ErrorSpider(Spider):
  handle_httpstatus_list = [404] 
  name = "error_spider"
  allowed_domains = ["amazon.com"]
  # Get the start URLs
  data = read_csv("skill_URLs.csv")
  start_urls = data['skill_link'].tolist()
  print(len(start_urls))

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.failed_urls = []

  @classmethod
  def from_crawler(cls, crawler, *args, **kwargs):
    spider = super(ErrorSpider, cls).from_crawler(crawler, *args, **kwargs)
    crawler.signals.connect(spider.handle_spider_closed, signals.spider_closed)
    return spider

  def parse(self, response):
    if response.status == 404:
        self.crawler.stats.inc_value('failed_url_count')
        self.failed_urls.append(response.url)

  def handle_spider_closed(self, reason):
    self.crawler.stats.set_value('failed_urls', ', '.join(self.failed_urls))

  def process_exception(self, response, exception, spider):
    ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
    self.crawler.stats.inc_value('downloader/exception_count', spider=spider)
    self.crawler.stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
