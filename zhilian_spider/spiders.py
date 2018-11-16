from bs4 import BeautifulSoup
from items import JobItem
from logger import logger_root


class ZhiLianSpider():
    def __init__(self, browser):
        self.browser = browser
        # self.count = -1
        self.current_page = 1

    def spider_item(self, page=None, start_page=None, end_page=None, start_item=None):
        if self.current_page < start_page:
            for i in range(start_page - self.current_page):
                try:
                    self.browser._wait_elem_by_class("soupager__btn")
                except Exception as e:
                    logger_root.exception(e)
                    pass
                button = self.browser.driver.find_element_by_css_selector("#pagination_content")
                next_button = button.find_elements_by_tag_name("button")[1]
                next_button.click()
                self.browser._switch_to_new_window()
                self.current_page += 1

        if not page:
            page = self.browser.driver.page_source
        bs_soup = BeautifulSoup(page, "lxml")
        list_items = bs_soup.find_all("div", class_="contentpile__content__wrapper__item__info")
        idx = 1
        if start_item:
            if int(start_item) < len(list_items):
                list_items = list_items[start_item:]
                idx = int(start_item)

        for idx, elem in enumerate(list_items, start=idx):
            try:
                JobItem(elem, self.browser)
                print("第{}页-第{}项".format(self.current_page, idx))
            except Exception as e:
                logger_root.exception(e)
                print("错误：{}--第{}页-第{}项".format(e.args, self.current_page, idx))
        if self.current_page > end_page:
            return None
        start_page += 1
        self.spider_item(start_page=start_page, end_page=end_page)
