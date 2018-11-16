from driver_browser import DriverClient
from spiders import ZhiLianSpider

url = "https://www.zhaopin.com/beijing/"
keys = ["python"]
browser = DriverClient(url)

print(browser.driver.title)
for key in keys:
    browser.search_key("python")
    page = browser.driver.page_source
    spider = ZhiLianSpider(browser)
    spider.spider_item(start_page=13, end_page=24, start_item=1)

    # spider.spider_item(browser.driver.page_source)
