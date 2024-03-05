from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Importa el módulo time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException


#opciones eager
options = Options()
#options.page_load_strategy = 'eager'
options.add_argument("--headless")  # Activa el modo sin cabeza


# Inicializa el WebDriver
#driver = webdriver.Chrome()
driver = webdriver.Chrome(options=options)# modo eager

# Navega al sitio web
driver.get("https://ventadebienes.bancobcr.com/wps/portal/bcrb/bcrbienes/bienes/Casas?&tipo_propiedad=1")

# Lista para almacenar los URLs
urls = []

# Bucle para navegar a través de las páginas

while True:
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bienImgBox a')))
        elementos = driver.find_elements(By.CSS_SELECTOR, 'div.bienImgBox a')
        for elemento in elementos:
            try:
                href = elemento.get_attribute('href')
                if href not in urls:  # Asegurar que no haya duplicados
                    urls.append(href)
                    #print(href)  # Imprime el href en vez del elemento para evitar el error al imprimir
            except StaleElementReferenceException:
                # Si el elemento se ha vuelto obsoleto, lo ignoramos y continuamos
                continue
        # Intenta navegar a la siguiente página
        next_button = driver.find_element(By.CSS_SELECTOR, 'li.page-item.next:not(.disabled) a.page-link')
        driver.execute_script("arguments[0].click();", next_button)
        WebDriverWait(driver, 10).until(EC.staleness_of(next_button))
    except NoSuchElementException:
        #print("Botón 'Siguiente' no encontrado, fin del recorrido.")
        break
    except Exception as e:
        print(f"Se encontró un error: {e}")
        break

# Cierra el navegador una vez finalizado el recorrido
driver.quit()

# Imprime la lista de URLs recolectadas
#for url in urls:
#    print(url)

# Al final de tu script, reemplaza el bucle de impresión con esto:
with open('urls.txt', 'w') as archivo:
    for url in urls:
        archivo.write(url + '\n')
