from selenium_functions import limpiar_output
from params import output_dir
from selenium_functions import consolidar
from sql_server import test
from bots.fbl5n_cierre.descargar_fbl5n_cierre import descargar_fbl5n_cierre

def descargar_recursivo(soc):
    try:
        descargar_fbl5n_cierre(soc)
    except Exception as e:
        print(e)
        descargar_recursivo(soc)


def fbl5n_cierre():
    # Limpiamos output antes de iniciar
    limpiar_output(output_dir)
    # Corremos for
    sociedades = [2000,2100,2200,3000,3100]


    for i in sociedades:
        descargar_recursivo(i)
        print(i)

    # Consolidamos en un solo archivo
    consolidado = consolidar(output_dir)
    consolidado.to_excel('consolidado.xlsx')
    #print('terminado')

    # SQL SERVER
    test(consolidado)    # Guardamos valores en SQL
    print('finalizado')