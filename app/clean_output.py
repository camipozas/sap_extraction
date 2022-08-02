import os
import shutil

from decorator import log


@log
def limpiar_output(output_dir):
    """
    If the output directory exists, delete it. If a file with the same name as the output directory
    exists, delete it. Create the output directory

    :param output_dir: The directory where the output files will be saved
    """
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
