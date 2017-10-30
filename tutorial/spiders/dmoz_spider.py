import scrapy
from scrapy.http import TextResponse
from scrapy.selector import Selector
from selenium import webdriver
import time
from pyvirtualdisplay import Display

#import items.py
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        #"https://www.tripadvisor.com/Restaurants-g304554-Mumbai_Bombay_Maharashtra.html"
        "https://www.tripadvisor.com/Restaurants-g298184-Tokyo_Tokyo_Prefecture_Kanto.html"
    ]
    def __init__(self):
        display = Display(visible=0, size=(800, 800))  
        display.start()
        self.browser = webdriver.Chrome('/opt/selenium_chrome/chromedriver')

    def parse(self, response):
        self.browser.get(response.url)
        time.sleep(5.0)
        body = self.browser.page_source
        sel_response = Selector(text=body)
        restro_list = sel_response.xpath('//*[@id="EATERY_SEARCH_RESULTS"]/div[contains(@class, "listing")]')
        l = "https://www.tripadvisor.com"
        # print('len', len(restro_list))
        f = open('data.csv', 'w+')
        for restro in restro_list:
            name = restro.xpath('div[2]/div/div[contains(@class, "title")]/a/text()').extract()[0].replace("\n","")
            link = l+restro.xpath('div[2]/div/div[contains(@class, "title")]/a/@href').extract()[0]
            print(name, link)
            f.write('"' + name.replace('"', '\\"') + '",' + link + "\n")
            f.flush()
        window_before = self.browser.window_handles[0]
        self.browser.execute_script('document.querySelector("a.nav.next").click();') 

        self.browser.switch_to_window(window_before)
        page_count = 0
        while True:
            page_count += 1
            print("page_count: ", page_count)
            time.sleep(5.0)
            body = self.browser.page_source
            sel_response = Selector(text=body)
            restro_list = sel_response.xpath('//*[@id="EATERY_SEARCH_RESULTS"]/div[contains(@class, "listing")]')
            l = "https://www.tripadvisor.com"
            for restro in restro_list:
                name = restro.xpath('div[2]/div/div[contains(@class, "title")]/a/text()').extract()[0].replace("\n","")
                link = l+restro.xpath('div[2]/div/div[contains(@class, "title")]/a/@href').extract()[0]
                print(name, link)
                f.write('"' + name.replace('"', '\\"') + '",' + link + "\n")
                f.flush()
            next = self.browser.find_element_by_xpath('//*[@id="EATERY_LIST_CONTENTS"]/div[3]/div/a[2]')
            if not next:
              break
            self.browser.execute_script('document.querySelector("a.nav.next").click();')
        self.browser.close()
