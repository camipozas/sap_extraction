import shutil
import os
import re

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

from params import output_dir, user_name, password, driver_path
from add_date import yesterday, today
from decorator import log


display = Display(visible=0, size=(1920, 1080))
display.start()
print('Initialized virtual display..')

# Folder tmp
options = webdriver.ChromeOptions() 
options.add_argument('--no-sandbox')
download_argument = f'download.default_directory={output_dir}'
prefs = {'download.default_directory' : output_dir}
options.add_experimental_option('prefs', prefs)

# Chequeo estado de la carga
@log
def chequear_estado(driver):
    try:
        error = driver.find_element_by_id("wnd[0]/sbar_msg-txt")
        displayed = error.is_displayed()
        error2 = driver.find_elements_by_class_name("sapUshellHeadTitle")
        ram = error2.is_displayed()
        if displayed or ram:
          text = error.get_attribute('innerHTML')
          text2 = error2.get_attribute('innerHTML')
          regex_vacio = r"No se ha seleccionado ninguna partida"
          regex_timeout = r"Tiempo de espera"
          regex_autorizacion = r"No tiene autorización para la sociedad"
          regex_ram = r"Cancel SAP"
          if re.match(regex_vacio, text):
           raise ValueError("Sin datos en sociedad")
          elif re.match(regex_timeout, text):
            raise ValueError('Error de SAP')
          elif re.match(regex_autorizacion, text):
            raise ValueError('Error autorización')
          elif re.match(regex_ram, text2):
            raise ValueError('RAM SAP')
    except NoSuchElementException:
        pass

# Ingreso a transacción y descarga
@log
def descarga(soc):
    #with webdriver.Chrome(driver_path, options = options) as driver:
      driver = webdriver.Chrome(options = options)
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
      ayer = yesterday()
      element = driver.find_element_by_id("M0:46:::12:34")    # Fecha
      element.click()
      element.clear()
      element.send_keys(ayer)
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

@log    
def limpiar_output(output_dir):
  # Si existe la carpeta la eliminamos
  if os.path.isdir(output_dir):
    shutil.rmtree(output_dir)
  # Si existe un archivo con el mismo nombre que la carpeta
  # lo eliminamos
  if os.path.isfile(output_dir):
    os.remove(output_dir)
  # Creamos la carpeta para que este limpia
  os.mkdir(output_dir)
  print('carpeta limpia')

@log
def consolidar(output_dir):
  df = pd.DataFrame()
  # Filtramos solo los archivos excel
  excels = [file for file in os.listdir(output_dir) if file.endswith('.xlsx')]
  excels_limpio = [ excel for excel in excels if not excel.startswith('export')]
  for excel in excels_limpio:
    # Leemos archivo
    tmp = pd.read_excel(os.path.join(output_dir, excel))

    if df.empty:
      df = tmp.copy()
    else:
      df = pd.concat([df, tmp])
      df['fecha_extraccion'] = today()
  return df