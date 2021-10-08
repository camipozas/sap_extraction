import shutil
import os
from datetime import datetime

import pandas as pd
from selenium import webdriver

from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display

from params import output_dir, user_name, password


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
def chequear_estado(driver):
    try:
        error1 = driver.find_element_by_id("wnd[0]/sbar_msg-txt")
        if error1.is_displayed():
           raise ValueError('Error de SAP')
    except NoSuchElementException:
        pass
    
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
      df['fecha_extraccion'] = datetime.today()
  return df