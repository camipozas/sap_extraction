import os

import pandas as pd

from add_date import today
from decorator import log


@log
def consolidar(output_dir):
    """
    It takes a directory as input, finds all the Excel files in that directory, reads them into a pandas
    DataFrame, and then concatenates them all together into a single DataFrame

    :param output_dir: The directory where the files are stored
    :return: A dataframe with all the data from the excel files in the output_dir
    """
    df = pd.DataFrame()
    # Filtramos solo los archivos excel
    excels = [file for file in os.listdir(
        output_dir) if file.endswith('.xlsx')]
    # excels_limpio = [excel for excel in excels if not excel.startswith('export')] # Esperando validación
    for excel in excels:
        # Leemos archivo
        tmp = pd.read_excel(os.path.join(output_dir, excel))

        if df.empty:
            df = tmp.copy()
        else:
            df = pd.concat([df, tmp])
            df['fecha_extraccion'] = today()
    return df
