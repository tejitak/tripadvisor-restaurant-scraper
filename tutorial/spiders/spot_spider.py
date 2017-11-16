import scrapy
from scrapy.http import TextResponse
from scrapy.selector import Selector
from selenium import webdriver
import time
from pyvirtualdisplay import Display

#import items.py
class SpotSpider(scrapy.Spider):
    name = "spot"
    allowed_domains = ["tripadvisor.com"]
    start_urls = [
        # "https://www.tripadvisor.com/Attractions-g293916-Activities-oa450-Bangkok.html#ATTRACTION_LIST"
        # "https://www.tripadvisor.com/Attractions-g293916-Activities-oa30-Bangkok.html"
        # "https://www.tripadvisor.com/Attractions-g293916-Activities-c47-Bangkok.html"
        "https://www.tripadvisor.com/Attractions-g293916-Activities-c20-Bangkok.html"
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
        spot_list = sel_response.xpath('//*[@id="ATTR_ENTRY_"]//div[contains(@class, "listing_details")]')
        l = "https://www.tripadvisor.com"
        # print('len', len(spot_list))
        f = open('data.csv', 'w+')
        for restro in spot_list:
            name = restro.xpath('div/div[contains(@class, "listing_title ")]/a/text()').extract()[0].replace("\n","")
            link = l+restro.xpath('div/div[contains(@class, "listing_title ")]/a/@href').extract()[0]
            print(name, link)
            f.write('"' + name.replace('"', '""') + '",' + link + "\n")
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
            spot_list = sel_response.xpath('//*[@id="ATTR_ENTRY_"]//div[contains(@class, "listing_details")]')
            l = "https://www.tripadvisor.com"
            for restro in spot_list:
                name = restro.xpath('div/div[contains(@class, "listing_title ")]/a/text()').extract()[0].replace("\n","")
                link = l+restro.xpath('div/div[contains(@class, "listing_title ")]/a/@href').extract()[0]
                print(name, link)
                f.write('"' + name.replace('"', '""') + '",' + link + "\n")
                f.flush()
            next = self.browser.find_element_by_xpath('//div[contains(@class, "unified pagination")]/a[contains(@class, "nav next rndBtn ui_button primary taLnk")]')
            if not next:
              break
            self.browser.execute_script('document.querySelector("a.nav.next").click();')
        self.browser.close()
