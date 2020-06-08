import scrapy
import tldextract
import os
from bs4 import BeautifulSoup

class MainSpider(scrapy.Spider):
    name = 'main'
    start_urls = []
    saved_pages = set()
    url = ''
    domain_with_subdomain = ''
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.url:
            print(self.url)
            self.start_urls.append(self.url)
        else:
            print('None url provided, using default one: http://kkio.pti.org.pl/2017/')
            self.start_urls.append('http://kkio.pti.org.pl/2017/')
        
        print(self.start_urls)
        
        extracted_url = tldextract.extract(self.start_urls[0])
        self.domain_with_subdomain = f'{extracted_url.subdomain}.{extracted_url.registered_domain}'
        print(self.domain_with_subdomain)
    
    def parse(self, response):
        current_url = response.request.url
        print("parse", current_url)
        
        hrefs = response.css('a::attr(href)').getall()
        
        filtered_hrefs_with_domain = self.filter_hrefs(hrefs, self.domain_with_subdomain)
        
        for href in filtered_hrefs_with_domain:
            yield response.follow(href, self.save_html)
            yield { 'link_within_domain': href}
            
    def filter_hrefs(self, hrefs, domain):
        filtered_hrefs_with_domain = filter(lambda href: domain in href or href.startswith('/'), hrefs)
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
        
        html_name = f'../public/{dirs}/page.html'
        # print(f'Html name: {html_name}')
        
        html_to_save = self.modify_hrefs_in_html(response.body, url_after_sufix)
        
        with open(html_name, "w", encoding='utf-8') as html_file:
            html_file.write(str(html_to_save))
        
        print('Saved html',url,len(self.saved_pages))
        
        yield scrapy.Request(url, callback=self.parse, dont_filter=True)
        
    def modify_hrefs_in_html(self, html, url_after_sufix):
        number_of_slashes = len(url_after_sufix.split('/'))
        is_url_ending_with_slash = url_after_sufix[len(url_after_sufix) - 1] == '/'
        
        if is_url_ending_with_slash:
            number_of_slashes = number_of_slashes - 1
        
        soup = BeautifulSoup(html)
        for a in soup.findAll('a', href=True):
            href = a['href']
            print(href)
            print(self.domain_with_subdomain in href)
            
            # absolute path
            if self.domain_with_subdomain in href:
                is_href_ending_with_slash = href[len(href) - 1] == '/'
                href_after_sufix = href.split('/', 3)[3]
                slashes = number_of_slashes*'../'
                if is_href_ending_with_slash:
                    href_after_sufix = f'./{slashes}{href_after_sufix}page.html'
                else:
                    href_after_sufix = f'./{slashes}{href_after_sufix}/page.html'
                print(href_after_sufix)
                a['href'] = href_after_sufix
            
            # relative path
            elif href.startswith('/'):
                is_href_ending_with_slash = href[len(href) - 1] == '/'
                slashes = number_of_slashes*'../'
                href_without_first_slash = href.split('/', 1)[1]
                if is_href_ending_with_slash:
                    href_after_sufix = f'./{slashes}{href_without_first_slash}page.html'
                else:
                    href_after_sufix = f'./{slashes}{href_without_first_slash}/page.html'
                print(href_after_sufix)
                a['href'] = href_after_sufix
        
        return soup
        