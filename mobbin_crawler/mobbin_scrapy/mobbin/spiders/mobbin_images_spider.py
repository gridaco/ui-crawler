# -*- coding: utf-8 -*-
import scrapy
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from time import sleep

from mobbin_crawler.mobbin_scrapy.mobbin.items import MobbinItem
from mobbin_crawler.mobbin_scrapy.mobbin.settings import IMAGES_STORE, BASE_DATA_PATH
from mobbin_crawler.mobbin_scrapy.mobbin_handler import MobbinHandle

MOBBIN_DATA_SOURCE = BASE_DATA_PATH.joinpath("mobbin")

class MobbinImagesSpiderSpider(scrapy.Spider):
    name = 'mobbin_images_spider'
    allowed_domains = ['mobbin.design']
    start_urls = ['https://mobbin.design/patterns']

    custom_settings = {
        "ITEM_PIPELINES": {'scrapy.pipelines.images.ImagesPipeline': 1},
        "IMAGES_STORE": MOBBIN_DATA_SOURCE.as_posix()
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")

        # options.headless = True
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        self.mobbin_handle = MobbinHandle(self.driver)
        self.mobbin_handle.auto_login()

    def parse(self, response):
        self.driver.get(response.url)
        curr_index = 0
        # Infinite scrolling
        while True:
            print("currIndex :: ", str(curr_index))
            result = self.mobbin_handle.get_n_screen_div(curr_index)
            if result["success"] is True:
                curr_index += 1

                # Enter Detail page by clicking item
                result["value"].click()
                sleep(0.1)

                # Parse data from detail page
                data = self.mobbin_handle.parse_detail()

                item = MobbinItem()
                item["url"] = data.url
                item["app_name"] = data.app
                item["app_desc"] = data.app_desc
                item["app_url"] = data.app_url
                item["category"] = data.category
                item["mobbin_patterns"] = data.mobbin_patterns
                item["mobbin_elements"] = data.mobbin_elements
                item["image_urls"] = [data.file_url]
                yield item


            # Exit Detail page by clicking 'X' button
                close_detail_button = self.driver.find_element_by_xpath(
                    "//button[@class='sc-erNlkL kveGTq sc-jzJRlG hvBLru']")
                close_detail_button.click()
                print("Close")
                sleep(0.1)
            else:
                print("Failed. Need to scroll down")
                # Control when to scroll
                scrolled = self.mobbin_handle.scroll_to_bottom()
                if scrolled:
                    sleep(0.2)
                else:
                    sleep(1)


if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'FEED_FORMAT': 'json',
        'FEED_URI': MOBBIN_DATA_SOURCE.joinpath("data.json").as_posix()
    })

    process.crawl(MobbinImagesSpiderSpider)
    process.start()  # the script will block here until the crawling is finished
