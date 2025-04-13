# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com/#')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "000E4D4C5559E35E50F614B04830E5FBE57D472FB946FB26C94B4BB645ADC395D24D077EFA66AC3E0D59FA9999E7A43DB34C5F431AD9BF27D7FA5BE1EB225CC6883494FCCA8089A5D10CC558764EFDE8E89FDF6BB6558092A65F5C3A6FC616B1313F9AA58BA9F7AB731B066DEB25135332FA5BAFC9F841E7F51386E31AC915E9F5FECD40A848372ACAE970A6AE1AADFBE592C14304815FD603EBDD436260485B67B49347C6D305913B1E461C1192A1F87C3728C153D2113169E3F14D90A85C98473CE7205BCBC40B0BFAE7AEDA75A3A4C9A86E32CD1E03466D083EB642CC5D0DB22DA94FC9F04AF8AF35D5C35D63C6738F3BE51269F5526C33CC755751B1D1CE26F273E2E11A748B6FE08CEEDC22249C15D5DB36E9FC0208C1EA940715E4683C951E2A22551C2CE0725A1DB6A438392A549B1777DB498D0E71715501FE6947030C576F1E2653344388D7FD7A674286518E56A43FB48F7480F1DEB9A097898FBF19"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
