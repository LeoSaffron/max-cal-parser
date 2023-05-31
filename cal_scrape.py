# -*- coding: utf-8 -*-
"""
Created on Mon May  2 00:24:27 2022

@author: hor
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import datetime
import os
import os.path
import random




uasd=""
pasd=""

month=12
year=2022
browser = "chrome"
# # browser = "firefox"


def generateRandomString(length):
    random_string = ''
    for _ in range(length):
        # Considering only upper and lowercase letters
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        # Convert to lowercase if the flip bit is on
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        # Keep appending random characters using chr(x)
        random_string += (chr(random_integer))
    return random_string

def getNewTempFolderDownloadPath(download_dir):
    os.path.join(r"\output_raw", generateRandomString(24)) 
    download_dir + generateRandomString(24) + r'\\'
    temp_folder_name =generateRandomString(24)
    os.mkdir(os.path.join("output_raw", "a" + temp_folder_name)) 
    path_temp_download_folder = r"\output_raw\a" + temp_folder_name + r"\\"
    return path_temp_download_folder

def openNewBrowserWindow(browser, download_dir):
    if browser == "firefox":
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.manager.showWhenStarting",False)
        fp.set_preference("browser.download.dir", download_dir)
        #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain")
        
        driver = webdriver.Firefox(firefox_profile=fp)
    # driver.maximize_window()
    
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        prefs = {"profile.default_content_settings.popups": 0,
                 # "download.default_directory": os.getcwd() + r"\temp_files_from_site\\", # IMPORTANT - ENDING SLASH V IMPORTANT
                 "download.default_directory": os.getcwd() + download_dir, # IMPORTANT - ENDING SLASH V IMPORTANT
                 "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)
        # driver = webdriver.Chrome(executable_path='./', chrome_options=options)
        driver = webdriver.Chrome(chrome_options=options)
    return driver


def scrape_files_into_a_temp_folder(month, year, user, passw, browser="chrome"):
    download_dir = r"\output_raw\\"
    download_dir = getNewTempFolderDownloadPath(download_dir)
    # os.mkdir(r"\output_raw\a" + generateRandomString(24)) 
    
    
    next_month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=32)
    next_month = next_month_date.month
    next_month_year = next_month_date.year
    
    month_item_in_list = "{0:0>2}".format(month)+str(year)
    next_month_item_in_list = "{0:0>2}".format(next_month)+str(next_month_year)
    
    next_month_date = datetime.datetime(month=month, year=year, day=1) + datetime.timedelta(days=32)
    
    driver = openNewBrowserWindow(browser, download_dir)
    
    ###################### LOGIN
    driver.get("https://www.cal-online.co.il/")
    time.sleep(5)
    driver.find_elements_by_class_name("logindesktop")[0].click()
    time.sleep(3)
    # iframe_login = driver.find_element_by_xpath('//iframe[@src="https://connect.cal-online.co.il/index.html"]')
    iframe_login = driver.find_element_by_xpath('//iframe[@src="/calconnect/index.html"]')
    time.sleep(2)
    driver.switch_to.frame(iframe_login)
    # driver.find_elements_by_xpath('//a[@href="/regular-login"]')[0].click()
    driver.find_elements_by_xpath('//a[@href="/calconnect/regular-login"]')[0].click()
    time.sleep(5)
    driver.find_element_by_id('mat-input-2').send_keys(user)
    time.sleep(1)
    driver.find_element_by_id('mat-input-3').send_keys(passw)
    time.sleep(1)
    driver.find_elements_by_xpath('//button[@type="submit"]')[0].click()
    driver.switch_to.default_content()
    time.sleep(10)
    
    ############# Close pop upabout new design
    try:
        wait = WebDriverWait(driver, 10)
        button_temp = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[aria-label="סגור חלון"]')))
        button_temp.click()
    except:
        pass
    
    ############# Get cards List
    try:
        wait = WebDriverWait(driver, 10)
        a_see_cards = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="צפייה בכרטיסים שלי - ניווט בתוך האתר"].ng-star-inserted')))
        a_see_cards.click()
    except:
        pass
    
    # Find the element containing the number
    card_number_element = driver.find_element(By.XPATH, '//span[@class="number"]')
    
    # Get the number
    first_card_number = card_number_element.text
    card_numbers_list = list(filter(lambda x: re.match(r'\d+', x), [x.text for x in driver.find_elements(By.XPATH, '//span[@class="number"]')]))
    
    
    
    
    
    try:
        # Wait for the button element to be clickable
        wait = WebDriverWait(driver, 10)
        button_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.close[title="סגירה"]')))
        button_element.click()
    except:
        pass
    
    
    driver.get("https://digital-web.cal-online.co.il/transactions-search")
    time.sleep(10)
    
    # Wait for the button element to be clickable
    wait = WebDriverWait(driver, 20)
    button_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'לצפייה בעסקאות')]")))
    
    # Click on the button
    button_element.click()
    
    
    ############### DOWNLOAD EXCEL FILE
    time.sleep(10)
        
    # Wait for the element to be clickable
    wait = WebDriverWait(driver, 20)
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='export-area']//span[contains(text(),'יצוא')]")))
    
    # Click on the element
    element.click()
    
    return download_dir




