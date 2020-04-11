import scrapy
import tldextract
import os

class MainSpider(scrapy.Spider):
    name = 'main'
    start_urls = ['http://kkio.pti.org.pl/2017/']
    saved_pages = set()
    
    def parse(self, response):
        current_url = response.request.url
        print("parse", current_url)
        
        hrefs = response.css('a::attr(href)').getall()
        
        extracted_url = tldextract.extract(self.start_urls[0])
        domain_with_subdomain = f'{extracted_url.subdomain}.{extracted_url.registered_domain}'
        
        filtered_hrefs_with_domain = self.filter_hrefs(hrefs, domain_with_subdomain)
        
        for href in filtered_hrefs_with_domain:
            yield response.follow(href, self.save_html)
            yield { 'link_within_domain': href}
            
    def filter_hrefs(self, hrefs, domain):
        filtered_hrefs_with_domain = filter(lambda href: domain in href, hrefs)
        filtered_hrefs_with_domain = filter(lambda href: href not in self.saved_pages, filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.pdf' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.jpg' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.jpeg' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.png' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.docx' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.doc' not in href.lower(), filtered_hrefs_with_domain)
        filtered_hrefs_with_domain = filter(lambda href: '.zip' not in href.lower(), filtered_hrefs_with_domain)
        return filtered_hrefs_with_domain
        
    def save_html(self, response):
        url = response.request.url
        
        self.saved_pages.add(url)
        print(len(self.saved_pages))
            
        url_after_sufix = url.split('/', 3)[3]
        
        dirs = f'../public/{url_after_sufix}'
        os.makedirs(dirs, exist_ok=True)
        
        html_name = f'../public/{dirs}page.html'
        # print(f'Html name: {html_name}')
        with open(html_name, 'wb') as html_file:
            html_file.write(response.body)
        
        print('Saved html',url,len(self.saved_pages))
        
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)