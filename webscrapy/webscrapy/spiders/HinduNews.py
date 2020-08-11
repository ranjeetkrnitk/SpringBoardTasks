import scrapy

class QuoteSpider(scrapy.Spider):
    name = "hindunews"
    start_urls = [
        'https://www.thehindu.com/news/national/?page=1'
    ]
    
    def parse(self,response):
        page = response.url.split("=")[-1]
        filename = 'hinduNews-%s.html' % page
        for cardnews in response.css("div.story-card-news"):
            #print("link", cardnews.css("a::attr(href)").extract()[-1])
            print("link", cardnews.css("a").get())

#Other-StoryCard

#story-card-news