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

driver = webdriver.Firefox(options=options)

# Fill in the start and end date
keywords   = "enchente"
start_date = "01/05/2024"
end_date   = "31/05/2024"

# test
print(keywords, start_date, end_date)
#sys.exit('so far, so good')

#input_data_inicio = driver.find_element(By.ID, "periodoIni")
#input_data_inicio.clear()
#input_data_inicio.send_keys(start_date)
#
#input_data_fim = driver.find_element(By.ID, "periodoFim")
#input_data_fim.clear()
#input_data_fim.send_keys(end_date)




# the ID of the hree inputs I got from the inspect code of the page
try:
    # Access the website
    driver.get("https://www.diariooficial.rs.gov.br/")
    human_delay(3, 6)

    # Locate and fill the keyword field
    search_field = driver.find_element(By.ID, "palavra-chave")  # Adjust the ID according to the actual field
    search_field.clear()
    search_field.send_keys(" OR ".join([kw.strip() for kw in keywords]))

    # Locate and fill the start date fieldstar
    start_date_field = driver.find_element(By.ID, "periodoIni")  # Adjust the ID
    start_date_field.clear()
    start_date_field.send_keys(start_date)

    # Locate and fill the end date field
    end_date_field = driver.find_element(By.ID, "periodoFim")  # Adjust the ID
    end_date_field.clear()
    end_date_field.send_keys(end_date)

    # test
    #print(keywords, start_date, end_date)

    # Click OK to submit search
    ok_button = driver.find_element(By.XPATH, '//input[@value="OK"]')
    ok_button.click()
    time.sleep(3)
    # so far, so good

    # Submit the form
    search_field.send_keys(Keys.RETURN)
    human_delay(3, 6)

    # Extract document links from the search results - parte critica
    
# >>>> baixar tudo - >>> ainda nao funciona <<<
    links = driver.find_elements(By.XPATH, "//a[contains(@href, 'diario_oficial')]")
    print(f"Found {len(links)} document links.")

    # Download each document
    for link in links:
        doc_url = link.get_attribute("href")
        if doc_url:
            print(f"Downloading: {doc_url}")
            try:
                response = requests.get(doc_url, stream=True)
                if response.status_code == 200:
                    file_name = os.path.join(output_dir, doc_url.split("/")[-1])
                    with open(file_name, "wb") as file:
                        for chunk in response.iter_content(chunk_size=1024):
                            file.write(chunk)
                    print(f"Saved: {file_name}")
                else:
                    print(f"Failed to download: {doc_url} (Status: {response.status_code})")
            except Exception as e:
                print(f"Error downloading {doc_url}: {e}")
        human_delay(2, 5)

finally:
    driver.quit()
