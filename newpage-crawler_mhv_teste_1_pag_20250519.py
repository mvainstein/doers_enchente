from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

dir_text = "document_texts"
dir_pdf  = "document_pdf"

for dir_name in [dir_text, dir_pdf]:
	if !os.path.isdir(dir_name):
		os.mkdir(dir_name)
		

geckodriver_path = "/snap/bin/firefox.geckodriver"
driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)
driver = webdriver.Firefox(service=driver_service)

#driver = webdriver.Firefox()  # or Chrome

#Exemplo qualquer
#driver.get("https://diariooficial.rs.gov.br/materia?id=1001975")  # replace with actual URL if needed

driver.get("https://diariooficial.rs.gov.br/materia?id=998884")

# Ordem de servico: leitor de pdf embutido na pag 

wait = WebDriverWait(driver, 5)


#driver.get(all_urls[0])
#results = wait.until(EC.presence_of_all_elements_located(
#        (By.ID, "formatacaotxt")
#    ))
#results = driver.find_element(By.ID, "formatacaotxt").text
#results1 = driver.find_element(By.ID, "formatacaotxt").text

results = driver.find_elements(By.ID, "formatacaotxt")
for r in results:
	print(r.text)

if (results == []):
	print("No text found")
else:
	print("Text found")

#print(results)
#print(results1)

wait = WebDriverWait(driver, 5)
driver.quit()  # 🧹 Cleanly close the browser no matter what


