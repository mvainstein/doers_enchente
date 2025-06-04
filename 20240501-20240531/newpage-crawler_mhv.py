from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
def human_delay(min_sec=2, max_sec=5):
    time.sleep(random.uniform(min_sec, max_sec))

geckodriver_path = "/snap/bin/firefox.geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=driver_service)

#driver = webdriver.Firefox()  # or Chrome
driver.get("https://www.diariooficial.rs.gov.br/")  # replace with actual URL if needed

wait = WebDriverWait(driver, 20)

# Step 1: Fill in the keyword
search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Digite"]')))
search_input.click()
keyword="enchente"
search_input.send_keys(keyword)

# Step 2: Fill in the start date
start_date_input = driver.find_element(By.XPATH, '//input[@placeholder="Data inicial"]')
start_date_input.click()
start_date_input.send_keys(Keys.CONTROL, "a")
start_date_input.send_keys("01/05/2024")

# Step 3: Fill in the end date
end_date_input = driver.find_element(By.XPATH, '//input[@placeholder="Data final"]')
end_date_input.click()
end_date_input.send_keys(Keys.CONTROL, "a")
end_date_input.send_keys("31/05/2024")

# Step 4: Wait until the search button is clickable and click it
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "botaoPesquisar")]')))
search_button.click()

### pagination and collection of urls

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

all_urls = []
page_number = 1  # Start from page 1

materia = 0

while True:
    # Wait for results to be present (ensure the page has loaded new results)
    wait = WebDriverWait(driver, 10)
    results = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, '//a[contains(@href, "materia?id=")]')
    ))

    # Collect URLs from the current page
    page_urls = [r.get_attribute("href") for r in results]
    all_urls.extend(page_urls)

    # Print progress (Optional)
    print(f"Collected {len(page_urls)} URLs from page {page_number}")

    try:
        # Locate the "Next" button (with aria-label="Next")
        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')

        # Click on the "Next" button using JavaScript (this bypasses the href issue)
        driver.execute_script("arguments[0].click();", next_button)

        # Wait for the new page to load (wait until old elements are no longer present)
        WebDriverWait(driver, 10).until(EC.staleness_of(results[0]))  # Wait until the first result is no longer present
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, '//a[contains(@href, "materia?id=")]')
        ))  # Wait for the new page results to load

        page_number += 1  # Increment page number

    except NoSuchElementException:
        print("Next button not found. Exiting...")
        break  # If the next button is not found, stop the loop

    except TimeoutException:
        print("Timeout while waiting for page load. Exiting...")
        break  # If page transition takes too long, stop the loop


driver.get(all_urls[0])


# Print all collected URLs
print(f"Total URLs collected: {len(all_urls)}")

# for url in all_urls:
#    print(url)


def save2file_urls(urls, filename='urls.txt'):
    with open(filename, 'w') as file:
        for url in urls:
            file.write(url + '\n')
# Function to save URLs to a file
namefile = 'DOERS_'+keyword+'.txt'
save2file_urls(all_urls, namefile)


#### Now go to each page to copy text
import os
import re # regular expressions

dir_text  = "document_texts"
dir_pdf   = "document_pdf"
idname    = "formatacaotxt"
classname = "conteudo" 

for dir_name in [dir_text, dir_pdf]:
	if not os.path.isdir(dir_name):
		os.mkdir(dir_name)
		
for url in all_urls:
	filename = re.search(r"materia.*$", url, re.IGNORECASE) # get last part of url that matches materia
	if filename:
		#print(filename.group()) # Output: "materia" until the end
		filename = filename.group() + '.txt'
		#print(filename)
	
	human_delay()
	driver.get(url)
	wait = WebDriverWait(driver, 10)
	# Find all text in page 
	results = driver.find_elements(By.ID, idname)
	#for r in results:
	#	print(r.text)	
	if (results == []):
		results = driver.find_elements(By.CLASS_NAME,classname)
	
	if (results == []):	
		print("No text found: " + filename )	
		with open(dir_pdf + '/' + filename, "w") as f:
			f.write("Please download pdf")
	else:
		#print("Text found")
		results_clean = []
		for r in results:
			results_clean.append(r.text)
		results_clean = set(results_clean) # Removes duplicates 
		
		with open(dir_text + '/' + filename, "w") as f:
			for r in results_clean:
				print(r,file=f) # Formatted
				#print(r.text,file=f) # Formatted
				#f.write(r.text)	 # Unformatted
		
		print(filename + " done")


driver.quit()  # 🧹 Cleanly close the browser no matter what


