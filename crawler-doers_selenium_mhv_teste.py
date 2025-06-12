from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import requests
import os
import sys

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))

from selenium.webdriver.firefox.options import Options
options = Options()
options.set_preference("general.useragent.override", 
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36")

# Create a directory to save downloaded files
output_dir = "downloaded_documents"
os.makedirs(output_dir, exist_ok=True)

# Input: Keywords and Date Range
#keywords = input("Enter keywords (comma-separated): ").split(",")
#start_date = input("Enter start date (dd/mm/yyyy): ")
#end_date = input("Enter end date (dd/mm/yyyy): ")

geckodriver_path = "/snap/bin/firefox.geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

#driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox(service=driver_service,options=options)

# Fill in the start and end date
keywords   = "enchente"
start_date = "01/05/2024"
end_date   = "31/05/2024"

# test
print(keywords, start_date, end_date)
#sys.exit('so far, so good')

input_data_inicio = driver.find_element(By.ID, "periodoIni")
input_data_inicio.clear()
input_data_inicio.send_keys(start_date)
#
input_data_fim = driver.find_element(By.ID, "periodoFim")
input_data_fim.clear()
input_data_fim.send_keys(end_date)




driver.quit()
