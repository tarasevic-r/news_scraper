from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DelfiSpider(CrawlSpider):
    name = 'crawler'
    allowed_domains = ['delfi.lt']
    start_urls = ['http://www.delfi.lt/']
    #base_url = 'http://www.delfi.lt/'
    delimiter = '\t'
    
    deny = ['delfi.lt/plius/', '/ru']
    rules = (
        Rule(LinkExtractor(restrict_css='h3.headline-title a'),
             callback='parse_item',
             follow=True),
        Rule(LinkExtractor(deny = deny),
             follow=False),
        Rule(LinkExtractor(restrict_css='.paging'),
             follow=True),
    )
    
    
    def parse_item(self, r):
        i = {}
        i['lead'] = r.css('.delfi-article-lead *::text').extract()
        i['image'] = r.css(
            'div.article-image div.image-article a.fancybox img').xpath('@src').extract()
        # i['body'] = r.xpath('//div[@class="article-body"]/div[@class="row"]/div[@class="col-xs-8"]/div/p/text()').extract()
        i['body'] = [
            ' '.join(
                line.strip() 
                for line in p.xpath('./p/text()').extract() 
                if line.strip()
            ) 
            for p in r.xpath('//div[@class="article-body"]/div[@class="row"]/div[@class="col-xs-8"]/div')
        ]
        
        return i
