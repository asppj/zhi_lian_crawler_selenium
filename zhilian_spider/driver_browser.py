import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class DriverClient():
    def __init__(self, url):
        self.driver = webdriver.Chrome()
        self.driver.get(url)
        self.curent_handle = self.driver.current_window_handle
        print(self.driver.current_window_handle)

    def search_key(self, key, class_name="zp-search__input"):
        input_elem = self.driver.find_element_by_class_name(class_name)
        input_elem.clear()
        input_elem.send_keys(key, Keys.ENTER)
        time.sleep(0.5)
        self._switch_to_new_window()
        self._wait_elem_by_id()

    def get(self, url):
        js = 'window.open("{}")'.format(url)
        self.driver.execute_script(js)
        self._switch_to_new_window()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "title")))
        time.sleep(0.4)
        print(self.driver.title)

        # time.sleep(5)
        # self.driver.get(url)
        # self._switch_to_new_window()

    def close(self):
        self.curent_handle = self.driver.current_window_handle
        self.driver.close()
        self._switch_to_new_window()

    def get_handles(self):
        return self.driver.window_handles

    def _switch_to_new_window(self):
        time.sleep(0.4)
        handles = self.get_handles()
        end = handles[-1]

        self.driver.switch_to.window(end)
        current_handle_new = self.driver.current_window_handle
        print("switch to {}".format(self.curent_handle, current_handle_new))
        self.curent_handle = current_handle_new
        pass

    def _wait_elem_by_id(self, id="listContent", seconds=10):
        locator = (By.ID, id)
        WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))
        print("elem:{} show".format(id))

    def _wait_elem_by_class(self, class_name, seconds=30):
        locator = (By.CLASS_NAME, class_name)
        WebDriverWait(self.driver, seconds).until(EC.presence_of_element_located(locator))

    @property
    def page_source(self):
        return self.driver.page_source
