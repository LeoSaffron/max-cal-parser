# -*- coding: utf-8 -*-
"""
Created on Mon May  2 03:02:36 2022

@author: hor
"""

from selenium import webdriver
import time
from binance.client import Client
import re
from glob import glob
import pickle
import datetime
from datetime import datetime
import datetime
import os
import os.path
from time import sleep


uasd=""
pasd=""
download_dir = "output_raw/"

month_names_he = {
 1: 'ינואר',
 2: 'פברואר',
 3: 'מרץ',
 4: 'אפריל',
 5: 'מאי',
 6: 'יוני',
 7: 'יולי',
 8: 'אוגוסט',
 9: 'ספטמבר',
 10: 'אוקטובר',
 11: 'נובמבר',
 12: 'דצמבר',
 }

def map_month_number_to_name_he(number):
    return month_names_he[number]

month=4
year=2022

next_month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=32)
next_month = next_month_date.month
next_month_year = next_month_date.year


next_2month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=63)
next_2month = next_2month_date.month
next_2month_year = next_2month_date.year

month_item_in_list = map_month_number_to_name_he(month) + " " + str(year)
next_month_item_in_list = map_month_number_to_name_he(next_month) + " " + str(next_month_year)
next_2month_item_in_list = map_month_number_to_name_he(next_2month) + " " + str(next_2month_year)

items_in_list_months = [month_item_in_list,
                        next_month_item_in_list,
                        next_2month_item_in_list]





fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", download_dir)
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

driver = webdriver.Firefox(firefox_profile=fp)
# driver.maximize_window()

###################### LOGIN
driver.get("https://www.max.co.il/homepage/welcome")
time.sleep(5)
driver.find_elements_by_xpath("//a[contains(., 'כניסה לאזור האישי')]")[1].click()
time.sleep(5)

driver.find_element_by_id("login-password-link").click()
time.sleep(5)

driver.find_element_by_id("user-name").send_keys(uasd)
time.sleep(1)
driver.find_element_by_id("password").send_keys(pasd)
time.sleep(1)

driver.find_elements_by_xpath("//span[contains(., 'כניסה לאזור האישי')]")[0].click()
time.sleep(10)

list_items_with_card_numbers = driver.find_elements_by_class_name("only-card-wrapper")[0].find_elements_by_tag_name("h4")

list_cards = []
for text_in_cards_list in list_items_with_card_numbers:
    list_cards.append(re.findall(r'[0-9]{4}', text_in_cards_list.text)[0])

# index_card = 0
for index_card in range(len(list_items_with_card_numbers)):
    print("card", list_cards[index_card])
    list_items_with_card_numbers = driver.find_elements_by_class_name("only-card-wrapper")[0].find_elements_by_tag_name("h4")
    list_items_with_card_numbers[index_card].click()
    time.sleep(10)
    
    for item_in_month_dropdown_list in items_in_list_months:
        #choose a month
        driver.find_elements_by_xpath("//div[@class='combo dates']"
              )[0].find_elements_by_class_name("open-menu")[0].click()
        time.sleep(1)
        print("item_in_month_dropdown_list", item_in_month_dropdown_list)
        driver.find_element_by_id("month-wrapper").find_elements_by_xpath("//li[contains(., '" + item_in_month_dropdown_list + "')]")[0].click()
        time.sleep(10)
        driver.find_elements_by_xpath("//span[@class='download-excel']")[0].click()
        time.sleep(10)
    driver.find_elements_by_xpath("//img[@src='/assets/images/homepage/max-logo.svg']")[0].click()
    time.sleep(10)







