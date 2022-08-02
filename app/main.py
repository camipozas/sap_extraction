from params import output_dir
from scrape_data import descarga
from sql_server import test
from decorator import log
from clean_output import limpiar_output
from consolidate import consolidar


@log
def descargar_recursivo(sociedades):
    """
    It tries to download the data recursively.

    :param sociedades: list of companies to download
    """
    try:
        descarga(sociedades)
    except ValueError("Sin datos en sociedad"):
        raise ValueError("SALTA CUENTA")
    except ValueError("RAM SAP"):
        descargar_recursivo(sociedades)
    except:
        descargar_recursivo(sociedades)


def main():
    """
    It downloads all the files from the website, consolidates them into one file, and then saves the
    consolidated file to SQL Server
    """
    # Limpiamos output antes de iniciar
    limpiar_output(output_dir)
    # Corremos for
    sociedades = [2000, 2100, 2200, 3000, 3100]

    for i in sociedades:
        try:
            descargar_recursivo(i)
        except:
            print(f"Sociedad {i}")
            continue
        print(i)

    # Consolidamos en un solo archivo
    consolidado = consolidar(output_dir)
    consolidado.to_excel('consolidado.xlsx')

    # SQL SERVER
    test(consolidado)    # Guardamos valores en SQL
    print('finalizado')


if __name__ == "__main__":
    main()
