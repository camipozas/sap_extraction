import os 
from environs import Env

# Credenciales
env = Env()
env.read_env()  # read .env file, if it exists

# SAP
user_name = env("user_name")  
password = env("password") 

# SQL
server_sql = env("server_sql") 
database = env("database")
user_sql = env("user_sql")
pass_sql = env("pass_sql")
mssql_driver = env("mssql_driver", "ODBC+Driver+17+for+SQL+Server")

# Output 
output_dir = os.path.join(os.getcwd(), 'output')