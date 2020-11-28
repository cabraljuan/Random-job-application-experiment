# -*- coding: utf-8 -*-
"""

@author: juan andrés cabral
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(ChromeDriverManager().install())


username=""
password=""
pagina=4
wage=15000
letter="Tengo 3 carreras hechas y sé inglés aleman ruso, frances y latin"
# Loop 

url="https://www.zonajobs.com.ar/"

# USER login
driver.get(url)
driver.find_element_by_class_name("ingresar").click() # Click to enter account
element = driver.find_element_by_id("username") 
element.send_keys(username) # Enter username
element = driver.find_element_by_id("password") 
element.send_keys(password) # Enter password
driver.find_element_by_id("loginButton").click() # Access


# OTRA PRUEBA
url = "https://www.zonajobs.com.ar/ofertas-de-empleo-publicacion-menor-a-15-dias-pagina-" + str(pagina) + ".html?recientes=true"    # Para buscar entre las publicaciones de los últimos 15 días
driver.get(url)
avisos = driver.find_element_by_class_name("aviso-no-sponsor") #Lista de avisos
links = avisos.find_elements_by_css_selector("a") # Links

for link in links:
    time.sleep(1)
    enlace = link.get_attribute('href')
    if type(enlace)==type(None):
                next
    else:
        if enlace.find('/empleos/') > 0: # Not all links are from jobs, we need to skip those
            driver.execute_script("window.open('');") # Perform all operations in a new window
            driver.switch_to.window(driver.window_handles[1])   # Switch to this window

            driver.get(enlace)
            time.sleep(1)
            
            # If already applied then skip
            if "POSTULADO" in driver.find_element_by_id("postulador").text:               
                driver.close() # Close window and go back to the previous
                driver.switch_to.window(driver.window_handles[0])
                next 
            else:
                time.sleep(1)
                driver.find_element_by_id("sueldoPretendido").clear() 
                driver.find_element_by_id("sueldoPretendido").send_keys(wage) # Wage
                time.sleep(1)
                driver.find_element_by_id("postularButton").click() # Send application
                time.sleep(2)
                # If additional information is required, then skip
                if "adicionales" in driver.find_element_by_class_name("modal-title").text:
                    driver.close() # Close window and go back to the previous
                    driver.switch_to.window(driver.window_handles[0])
                    next
                else:
                    driver.switch_to.frame("carta_ifr")  # Switch to application letter
                    driver.find_element_by_id("tinymce").send_keys(letter)  # Put text
                    driver.switch_to.default_content() # Switch again to default content
                    
                    submit_button = driver.find_element_by_xpath( # Submit button
                            '//*[@id="form-carta-de-postulacion"]/div/div[2]/div/button[1]') 
                    submit_button.click() # Submit
                    time.sleep(1)
                    driver.close() # Close window and go back to the previous
                    driver.switch_to.window(driver.window_handles[0])


