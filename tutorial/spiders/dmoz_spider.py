import scrapy
from scrapy.http import TextResponse
from scrapy.selector import Selector
from selenium import webdriver
from selenium import selenium
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
#import items.py
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        "https://www.tripadvisor.com/Restaurants-g304554-Mumbai_Bombay_Maharashtra.html"
    ]
    def __init__(self):
    	binary = FirefoxBinary('/opt/selenium_firefox/firefox/firefox')
        self.browser = webdriver.Firefox(firefox_binary=binary)

    def parse(self, response):
        #namelist = response.xpath('//*[contains(@class,"property_title")]/text()').extract()
        #linklist = response.xpath('//*[contains(@class,"property_title")]/@href').extract()
        self.browser.get(response.url)
        time.sleep(2.0)
        body = self.browser.page_source
        sel_response = Selector(text=body)
        restro_list = sel_response.xpath('//*[@id="EATERY_SEARCH_RESULTS"]/div/div[2]')
        l = "https://www.tripadvisor.com"
        	#print len(restro_list)
        f = open('data.csv', 'w+')
        for restro in restro_list:
        	name = restro.xpath('h3/a/text()').extract()[0].replace("\n","")
        	link = l+restro.xpath('h3/a/@href').extract()[0]
        	review1 = restro.xpath('ul/li[1]/span/a/text()').extract()[0]
        	review2 = restro.xpath('ul/li[2]/span/a/text()').extract()[0]
        	f.write(name.encode('utf-8')+","+link.encode('utf-8')+","+review1.encode('utf-8')+","+review2.encode('utf-8')+"\n")
        	f.flush()
        next = self.browser.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[3]/div/a')
        window_before = self.browser.window_handles[0]
        next.click()

        self.browser.switch_to_window(window_before)
        while True:
        	
        	time.sleep(2.0)
        	body = self.browser.page_source
        	sel_response = Selector(text=body)
        	restro_list = sel_response.xpath('//*[@id="EATERY_SEARCH_RESULTS"]/div/div[2]')
        	l = "https://www.tripadvisor.com"
        	#print len(restro_list)
        	for restro in restro_list:
        		name = restro.xpath('h3/a/text()').extract()[0].replace("\n","")
        		link = l+restro.xpath('h3/a/@href').extract()[0]
        		if(len(restro.xpath('ul/li')))>=2:
	        		review1 = restro.xpath('ul/li[1]/span/a/text()').extract()[0]
	        		review2 = restro.xpath('ul/li[2]/span/a/text()').extract()[0]
	        		f.write('"'+name.encode('utf-8')+'","'+link.encode('utf-8')+'","'+review1.encode('utf-8')+'","'+review2.encode('utf-8')+'"\n')
	        		f.flush()
	        	elif len(restro.xpath('ul/li'))>0:
	        		review1 = restro.xpath('ul/li[1]/span/a/text()').extract()[0]
	        		#review2 = restro.xpath('ul/li[2]/span/a/text()').extract()[0]
	        		f.write('"'+name.encode('utf-8')+'","'+link.encode('utf-8')+'","'+review1.encode('utf-8')+'"\n')
	        		f.flush()
	        	else:
	        		#review1 = restro.xpath('ul/li[1]/span/a/text()').extract()[0]
	        		#review2 = restro.xpath('ul/li[2]/span/a/text()').extract()[0]
	        		f.write('"'+name.encode('utf-8')+'","'+link.encode('utf-8')+'"\n')
	        		f.flush()
        	next = self.browser.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[3]/div/a[2]')
        	next.click()
        self.browser.close()




        	


        


