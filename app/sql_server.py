from sqlalchemy import create_engine
import pandas as pd
from params import server_sql, database, user_sql, pass_sql, mssql_driver
from decorator import log


@log
# Establecemos conexión con SQL Server
def connection():
    """
    This function creates a connection to the SQL Server database using the pyodbc library
    :return: The engine is being returned.
    """
    engine = create_engine(f'mssql+pyodbc://{user_sql}:{pass_sql}@{server_sql}/{database}?driver={mssql_driver}',
                           fast_executemany=True)
    return engine


@log
# Probamos conexión a SQL Server y la respectiva tabla, si existe reemplazamos los valores.
def test(df):
    """
    It takes a dataframe, writes it to a SQL table, and then executes a stored procedure

    :param df: The dataframe you want to insert into the database
    """
    engine = connection()
    df.to_sql('data_diaria_fbl5n', con=engine,
              if_exists='replace', index=False)
    engine.execute("exec [Estado_morosidad]")
    print('ejecutado')
