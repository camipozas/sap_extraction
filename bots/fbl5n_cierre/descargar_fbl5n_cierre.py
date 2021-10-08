from datetime import datetime,timedelta

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from params import output_dir, user_name, password
from selenium_functions import chequear_estado


# Folder tmp
options = webdriver.ChromeOptions() 
options.add_argument('--no-sandbox')
download_argument = f'download.default_directory={output_dir}'
prefs = {'download.default_directory' : output_dir}
options.add_experimental_option('prefs', prefs)

# Ingreso a transacción y descarga
def descarga(soc):
    driver = webdriver.Chrome(options = options)

    #   Ingresar a SAP
    driver.get("https://dims4prdci.dimerc.cl:8001/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html#Shell-startGUI?sap-ui2-tcode=FBL5N&sap-system=PRDCLNT300")
    element = driver.find_element_by_id("USERNAME_FIELD-inner")
    element.send_keys(user_name)
    element = driver.find_element_by_id("PASSWORD_FIELD-inner")
    element.send_keys(password)
    element.send_keys(Keys.RETURN)

    #   Ingresar a la transaccion
    driver.implicitly_wait(20)
    driver.switch_to.frame("application-Shell-startGUI")    # Frames SAP (tener ojo con roles y perfiles)
    driver.switch_to.frame("ITSFRAME1")

    # Llenar datos
    chequear_estado(driver)
    element = driver.find_element_by_id("M0:46:::2:34") # Sociedad
    element.send_keys(soc)
    layout = "/AUTOMATI"    # Layout
    element = driver.find_element_by_id("M0:46:::30:34")
    element.clear()
    element.send_keys(layout)
    # Cálculo último día del mes
    today = datetime.date.today()
    first = today.replace(day=1)
    eopm = first - datetime.timedelta(days=1)
    eopm = eopm.strftime("%d.%m.%Y")
    element = driver.find_element_by_id("M0:46:::12:34")    # Fecha
    element.click()
    element.clear()
    element.send_keys(eopm)
    chequear_estado(driver)

    try:
        element = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.ID, "M0:50::btn[8]")) #This is a dummy element
        )
        element = driver.find_element_by_id("M0:50::btn[8]")    # Ejecutar
        if element.is_displayed() and element.is_enabled():
            element.click() # this will click the element if it is there
            print("FOUND THE LINK CREATE ACTIVITY! and Clicked it!")
    except NoSuchElementException:
        print("...")

    #   Descargar
    #   Esperar a que se procesen los datos, si se demora más de 1000 segundos, falla.
    element = WebDriverWait(driver, 1000).until(
    EC.presence_of_element_located((By.ID, "M0:46:::1:0_l")) #This is a dummy element
    )
    # Scrollbar, mapeo para extraer datos
    element = driver.find_element_by_id("RCua2FioriToolbar-moreButton")
    element.click()

    element = driver.find_element_by_id("wnd[0]/mbar/menu[0]-BtnChoiceMenu")
    element.location_once_scrolled_into_view
    element.click()

    element = driver.find_element_by_id("wnd[0]/mbar/menu[0]/menu[3]")
    element.click()


    element = driver.find_element_by_id("wnd[0]/mbar/menu[0]/menu[3]/menu[1]")
    element.click()

    driver.implicitly_wait(10)

    #   Espera a que se abra dialogo
    WebDriverWait(driver, 600).until(
    EC.presence_of_element_located((By.ID, "PromptDialogOk-cnt"))
    )
    button = driver.find_element_by_id("PromptDialogOk")
    
    #   No se por qué pero con dos click funciona
    try:
        button.click()
        button.click()
    except:
        try:
            driver.implicitly_wait(10)
            button = driver.find_element_by_id("PromptDialogOk")
            button.click()
            button.click()
        except:
            print('error')
    finally:
        driver.quit()