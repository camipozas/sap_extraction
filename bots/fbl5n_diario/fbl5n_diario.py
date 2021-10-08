from selenium_functions import limpiar_output
from params import output_dir
from selenium_functions import consolidar
from sql_server import test
from bots.fbl5n_diario.descargar_fbl5n_diario import descargar_fbl5n_diario

def descargar_recursivo(soc):
    try:
        descargar_fbl5n_diario(soc)
    except Exception as e:
        print(e)
        descargar_recursivo(soc)


def fbl5n_diario():
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