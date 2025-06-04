from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import re # regular expressions


dir_text = "document_texts"
dir_pdf  = "document_pdf"

for dir_name in [dir_text, dir_pdf]:
	if not os.path.isdir(dir_name):
		os.mkdir(dir_name)
		

geckodriver_path = "/snap/bin/firefox.geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=driver_service)

#driver = webdriver.Firefox()  # or Chrome

# Exemplo com texto => id = "formatacaotxt"
#idname = "formatacaotxt"
#url = "https://diariooficial.rs.gov.br/materia?id=1001975"

idname="conteudo"
#url = "https://diariooficial.rs.gov.br/materia?id=1001531"

#url = "https://diariooficial.rs.gov.br/materia?id=999540"
url = "https://diariooficial.rs.gov.br/materia?id=1161577"

# Exemplo com pdf # Ordem de servico: leitor de pdf embutido na pag 
#driver.get("https://diariooficial.rs.gov.br/materia?id=998884")
#idname = "viewer" #"page" #"textLayer"
#url = "https://diariooficial.rs.gov.br/materia?id=998884"


filename = re.search(r"materia.*$", url, re.IGNORECASE)
if filename:
	#print(filename.group()) # Output: "materia" until the end
	filename = filename.group() + '.txt'
	#print(filename)
	

driver.get(url)

wait = WebDriverWait(driver, 5)

# Find all text in page 
#results = driver.find_elements(By.ID, idname)

#if (results == []):
results = driver.find_elements(By.CLASS_NAME,idname)
#print(len(results))

#for r in results:
#	print(r.text)
	
#print("******")

resultado = []
for r in results:
	resultado.append(r.text)
	
resultado = set(resultado) # set: remove duplicates	

for r in resultado:
	print(r)
		
	
'''
if (results == []):
	print("No text found")	
	with open(dir_pdf + '/' + filename, "w") as f:
		f.write("Please download pdf")
else:
	#print("Text found")
	with open(dir_text + '/' + filename, "w") as f:
		for r in results:
			print(r.text,file=f) # Formatted
			#f.write(r.text)	 # Unformatted
'''

wait = WebDriverWait(driver, 5)
driver.quit()  # 🧹 Cleanly close the browser no matter what

