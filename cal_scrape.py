# -*- coding: utf-8 -*-
"""
Created on Mon May  2 00:24:27 2022

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

month=4
year=2022

next_month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=32)
next_month = next_month_date.month
next_month_year = next_month_date.year

month_item_in_list = "{0:0>2}".format(month)+str(year)
next_month_item_in_list = "{0:0>2}".format(next_month)+str(next_month_year)

next_month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=32)

fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.manager.showWhenStarting",False)
fp.set_preference("browser.download.dir", download_dir)
#fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")

driver = webdriver.Firefox(firefox_profile=fp)
# driver.maximize_window()

###################### LOGIN
driver.get("https://www.cal-online.co.il/")
time.sleep(5)
driver.find_elements_by_class_name("logindesktop")[0].click()
time.sleep(3)
iframe_login = driver.find_element_by_xpath('//iframe[@src="https://connect.cal-online.co.il/index.html"]')
time.sleep(2)
driver.switch_to.frame(iframe_login)
driver.find_elements_by_xpath('//a[@href="/regular-login"]')[0].click()
time.sleep(5)
driver.find_element_by_id('mat-input-2').send_keys(uasd)
time.sleep(1)
driver.find_element_by_id('mat-input-3').send_keys(pasd)
time.sleep(1)
driver.find_elements_by_xpath('//button[@type="submit"]')[0].click()
driver.switch_to.default_content()
time.sleep(10)



############# Get cards List
driver.find_elements_by_xpath('//a[@href="CardDetails.aspx?action=2"]')[0].click()
time.sleep(3)
driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_rdoTransactionDate').click()
time.sleep(5)

driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_lblCollapse").click()
time.sleep(1)

# driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_pnlMain")

list_cards = []

list_items_with_card_numbers = driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_pnlMain"
                          ).find_elements_by_class_name('categoryItem')
for text_in_cards_list in list_items_with_card_numbers:
    list_cards.append(re.findall(r'[0-9]{4}', text_in_cards_list.text)[0])


driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_lblCollapse").click()
time.sleep(1)



############### DOWNLOAD EXCEL FILE PER CARD

for index_card in range(len(list_cards)):
    driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_lblCollapse").click()
    driver.find_element_by_id("ctl00_ContentTop_cboCardList_categoryList_pnlMain"
                              ).find_elements_by_class_name('categoryItem')[index_card].click()
    

    
    
    ##select currect month
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlMonthYearList_Button').click()
    time.sleep(1)
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlMonthYearList_OptionList'
                              ).find_elements_by_xpath('li[@value="' + month_item_in_list + '"]')[0].click()
    time.sleep(1)
    
    ##select 1st day in the dropdown list in the start date
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlDaysList_Button').click()
    time.sleep(1)
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeStart_ctlDaysList_OptionList'
                              ).find_elements_by_xpath('li[@value="1"]')[0].click()
    time.sleep(1)
    
    
    
    ##select next month
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlMonthYearList_Button').click()
    time.sleep(1)
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlMonthYearList_OptionList'
                              ).find_elements_by_xpath('li[@value="' + next_month_item_in_list + '"]')[0].click()
    
    ##select 1st day in the dropdown list in the end date
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlDaysList_Button').click()
    time.sleep(1)
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlDateScopeEnd_ctlDaysList_OptionList'
                              ).find_elements_by_xpath('li[@value="1"]')[0].click()
    time.sleep(1)
    
    
    driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlSubmitRequest').click()
    time.sleep(10)
    
    
    #click on export to excel button
    try:
        driver.find_element_by_id('ctl00_FormAreaNoBorder_FormArea_ctlMainToolBar_btnExcel').click()
        print('Downloaded xls for card {}'.format(list_cards[index_card]))
    except:
        try:
            if driver.find_elements_by_xpath("//span[@class='vld_summary']")[0].text == 'לא נמצאו נתונים':
                print('no records for card {}'.format(list_cards[index_card]))
            else:
                print('Some error occured for card {}'.format(list_cards[index_card]))
                print('Error on the screen: {}'.format(driver.find_elements_by_xpath("//span[@class='vld_summary']")[0].text))
        except:
            print('Some error occured for card {}'.format(list_cards[index_card]))
            
                





