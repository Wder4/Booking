# -*- coding: utf-8 -*-

from Module import Bookingcom
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from time import sleep


class access:
    def __init__(self):
        pass

    def Choose_Date(self):
        # path = r'C:\Users\james\Desktop\python\chromedriver.exe'
        # # opts = Options()
        # # opts.add_argument('--incognito')
        # # opts.add_argument('User-Agent={}'.format(UserAgent().random))
        # # opts.add_argument('--headless')
        # # opts.add_argument("--start-maximized")
        # # driver = webdriver.Chrome(path, options=opts)
        # driver = webdriver.Chrome(path)
        # url = 'https://www.booking.com/index.zh-tw.html?aid=304142&label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEXyAEM2AEB6AEB-AELiAIBqAIDuAKCmuHpBcACAQ&sid=ddc56f2808b2bac0f809bf277599e6ca&srpvid=4c975dacefd2008c&click_from_logo=1'
        # driver.get(url)
        # where = driver.find_element_by_xpath('//*[@id="ss"]')
        # where.send_keys('大阪')
        # where.send_keys(Keys.RETURN)
        # driver.find_element_by_xpath('//*[@id="frm"]/div[1]/div[2]/div[1]/div[2]/div/div/div/div/button').click()
        # driver.find_element_by_link_text('25')

    def Station_Dist(self):
        pass

if __name__ == '__main__':
    obj = access()
    # obj.Choose_Date()



