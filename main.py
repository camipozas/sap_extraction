from selenium_functions import limpiar_output
from params import output_dir
from selenium_functions import descarga
from selenium_functions import consolidar
from sql_server import test
from decorator import log

# Credenciales
from params import (
  user_name,
  password,
  server_sql,
  database,
  user_sql,
  pass_sql
)

# Limpiamos output antes de iniciar
limpiar_output(output_dir)
# Corremos for
sociedades = [2100,2200,3000,3100]

@log
def descargar_recursivo(sociedades):
  try:
     descarga(sociedades)
  except ValueError("Sin datos en sociedad"):
    raise ValueError("SALTA CUENTA")
  except ValueError("RAM SAP"):
   descargar_recursivo(sociedades)
  except:
     descargar_recursivo(sociedades)

for i in sociedades:
    try:
      descargar_recursivo(i)
    except:
      print(f"salta sociedad {i}")
      continue
    print(i)

# Consolidamos en un solo archivo
consolidado = consolidar(output_dir)
consolidado.to_excel('consolidado.xlsx')

# SQL SERVER
test(consolidado)    # Guardamos valores en SQL
print('finalizado')