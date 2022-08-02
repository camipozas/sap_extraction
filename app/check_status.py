import re

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from decorator import log


@log
def chequear_estado(driver):
    """
    It checks if there's an error message displayed in the SAP screen, and if there is, it raises an
    exception

    :param driver: the webdriver object
    """
    try:
        error = driver.find_element(By.ID, "wnd[0]/sbar_msg-txt")
        displayed = error.is_displayed()
        error2 = driver.find_element(By.CLASS_NAME, "sapUshellHeadTitle")
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
