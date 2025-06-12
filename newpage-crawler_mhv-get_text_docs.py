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

all_urls = []

materia = 0

keyword = "enchente"
start_line = 114
namefile = 'DOERS_'+keyword+'.txt'

with open(namefile) as file:
	lines = [line.rstrip() for line in file]

all_urls = lines[start_line-1:]

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

n = 1		
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
		print(str(n) + " ***** No text found: " + filename )	
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
		
		print(str(n)+ "  " + filename + " done!")
		
	n = n + 1


driver.quit()  # 🧹 Cleanly close the browser no matter what


