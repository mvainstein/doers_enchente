from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
def human_delay(min_sec=3, max_sec=7):
    time.sleep(random.uniform(min_sec, max_sec))

geckodriver_path = "/snap/bin/firefox.geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=driver_service)

#driver = webdriver.Firefox()  # or Chrome
driver.get("https://www.diariooficial.rs.gov.br/")  # replace with actual URL if needed

wait = WebDriverWait(driver, 20)

# Step 1: Fill in the keyword
search_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Digite"]')))
human_delay()
search_input.click()
keyword="enchente"
human_delay()
search_input.send_keys(keyword)

# Step 2: Fill in the start date
start_date_input = driver.find_element(By.XPATH, '//input[@placeholder="Data inicial"]')
human_delay()
start_date_input.click()
start_date_input.send_keys(Keys.CONTROL, "a")
human_delay()
start_date_input.send_keys("01/05/2024")
#start_date_input.send_keys("01/06/2024")

# Step 3: Fill in the end date
end_date_input = driver.find_element(By.XPATH, '//input[@placeholder="Data final"]')
human_delay()
end_date_input.click()
end_date_input.send_keys(Keys.CONTROL, "a")
human_delay()
end_date_input.send_keys("31/05/2024")
#end_date_input.send_keys("21/05/2025")

# Step 4: Wait until the search button is clickable and click it
search_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "botaoPesquisar")]')))
human_delay()
search_button.click()

### pagination and collection of urls

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import subprocess

def download_file_with_wget(url, output_path=None):
    """Downloads a file using wget.

    Args:
        url: The URL of the file to download.
        output_path: The path where the file should be saved.
                     If None, the file will be saved with the name
                     from the url in the current directory.
    """
    command = ["wget", url]
    if output_path:
        command.extend(["-O", output_path])
    try:
        subprocess.run(command, check=True)
        print(f"File downloaded successfully to: {output_path or url.split('/')[-1]}")
    except subprocess.CalledProcessError as e:
        print(f"Error downloading file: {e}")




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
		human_delay()
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
dir_html  = "document_html"
#idname    = "formatacaotxt" # talvez nao seja necessario
classname = "conteudo"
tipo   = "assunto"
data   = "data"
autor  = "responsavel"
 

for dir_name in [dir_text, dir_pdf,dir_html]:
	if not os.path.isdir(dir_name):
		os.mkdir(dir_name)

n = 1		
for url in all_urls:
	filename = re.search(r"materia.*$", url, re.IGNORECASE) # get last part of url that matches materia
	ID = re.search(r"=.*$", url, re.IGNORECASE) # get last part of url that matches =
	ID = ID.group()
	ID = ID[1:]
	if filename:
		human_delay()
		download_file_with_wget(url, output_path = dir_html + '/' + filename.group() + '.html')
		#print(filename.group()) # Output: "materia" until the end
		filename = filename.group() + '.txt'
		#print(filename)
		
	
	human_delay()
	driver.get(url)
	wait = WebDriverWait(driver, 10)
	# Find all text in page 
	#results = driver.find_elements(By.ID, idname)
	##for r in results:
	##	print(r.text)	
	#if (results == []):
	#	results = driver.find_elements(By.CLASS_NAME,classname)
	
	# Find all text in page 
	#results = driver.find_elements(By.ID, idname)
	#for r in results:
	#	print(r.text)	
	#if (results == []):
	data_text = driver.find_elements(By.CLASS_NAME,data)
	tipo_text = driver.find_elements(By.CLASS_NAME,tipo)
	autor_text = driver.find_elements(By.CLASS_NAME,autor)
	results = driver.find_elements(By.CLASS_NAME,classname)
		
	
	if (results == []):	
		print(str(n) + " ***** No text found: " + filename )	
		with open(dir_pdf + '/' + filename, "w") as f:
			f.write("Please download pdf")
	else:
		#print("Text found")
		results_clean = []
		for r in results:
			results_clean.append(r.text)
		results_clean = set(results_clean) # Removes duplicates 
		
		data_text_clean = []
		for r in data_text:
			data_text_clean.append(r.text)
		data_text_clean = set(data_text_clean)
		
		tipo_text_clean = []
		for r in tipo_text:
			tipo_text_clean.append(r.text)
		tipo_text_clean = set(tipo_text_clean)
			
		autor_text_clean = []
		for r in autor_text:
			autor_text_clean.append(r.text)
		autor_text_clean = set(autor_text_clean)
		
		with open(dir_text + '/' + filename, "w") as f:
			for r in results_clean:
				print(r,file=f) # Formatted
				#print(r.text,file=f) # Formatted
				#f.write(r.text)	 # Unformatted
		
		print(str(n)+ "  " + filename + " done!")
		
		
		with open(dir_text + '/' + "dados_documentos.csv", "a") as f:
			print(ID+';'+str(data_text_clean)+';'+str(tipo_text_clean)+';'+str(autor_text_clean),file=f)
		
	n = n + 1


driver.quit()  # 🧹 Cleanly close the browser no matter what


