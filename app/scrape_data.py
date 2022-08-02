from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager

from params import output_dir, user_name, password
from add_date import yesterday
from decorator import log
from check_status import chequear_estado

options = Options()
options.headless = False
options.add_argument("--window-size=1920,1200")

# Folder tmp
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
download_argument = f'download.default_directory={output_dir}'
prefs = {'download.default_directory': output_dir}
options.add_experimental_option('prefs', prefs)


def descarga(soc):

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=options)

    driver.get("https://dims4prdci.dimerc.cl:8001/sap/bc/ui5_ui5/ui2/ushell/shells/abap/FioriLaunchpad.html#Shell-startGUI?sap-ui2-tcode=FBL5N&sap-system=PRDCLNT300")
    element = driver.find_element(By.ID, "USERNAME_FIELD-inner")
    element.send_keys(user_name)
    element = driver.find_element(By.ID, "PASSWORD_FIELD-inner")
    element.send_keys(password)
    element.send_keys(Keys.RETURN)
    #   Ingresar a la transaccion
    driver.implicitly_wait(20)
    # Frames SAP (tener ojo con roles y perfiles)
    driver.switch_to.frame("application-Shell-startGUI")
    driver.switch_to.frame("ITSFRAME1")

    # Llenar datos
    chequear_estado(driver)
    element = driver.find_element(By.ID, "M0:46:::2:34")  # Sociedad
    element.send_keys(soc)
    layout = "/AUTOMATI"    # Layout
    element = driver.find_element(By.ID, "M0:46:::30:34")
    element.clear()
    element.send_keys(layout)
    ayer = yesterday()
    element = driver.find_element(By.ID, "M0:46:::12:34")    # Fecha
    element.click()
    element.clear()
    element.send_keys(ayer)
    chequear_estado(driver)

    try:
        element = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located(
                (By.ID, "M0:50::btn[8]"))  # This is a dummy element
        )
        element = driver.find_element(By.ID, "M0:50::btn[8]")    # Ejecutar
        if element.is_displayed() and element.is_enabled():
            element.click()  # this will click the element if it is there
            print("FOUND THE LINK CREATE ACTIVITY! and Clicked it!")
    except NoSuchElementException:
        print("...")

        #   Descargar
        #   Esperar a que se procesen los datos, si se demora más de 1000 segundos, falla.
    element = WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located(
            (By.ID, "M0:46:::1:0_l"))  # This is a dummy element
    )
    # Scrollbar, mapeo para extraer datos
    element = driver.find_element(By.ID, "RCua2FioriToolbar-moreButton")
    element.click()

    element = driver.find_element(By.ID,
                                  "wnd[0]/mbar/menu[0]-BtnChoiceMenu")
    element.location_once_scrolled_into_view
    element.click()

    element = driver.find_element(By.ID, "wnd[0]/mbar/menu[0]/menu[3]")
    element.click()

    element = driver.find_element(By.ID,
                                  "wnd[0]/mbar/menu[0]/menu[3]/menu[1]")
    element.click()

    driver.implicitly_wait(10)

    #   Espera a que se abra dialogo
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "PromptDialogOk-cnt")))
    driver.quit()
