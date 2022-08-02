# SAP EXTRACTION FBL5N

## English Version

> Spanish version / Versión en español [aquí](/docs/spanish.md).

This is a bot for the extraction in SAP Fiori transaction.

Fistable, I defined the function *descarga()* that enters in the transaction in SAP by selenium I did the all scraping to do all the flow and extract the data.

Notably SAP have frames, that is websites inside another websites so we have to used switch to enterokay.

Secondly, the individually downloads files were hosted in a temporary folder in the same code, where once all the files consolidated, they are deleted. This consolidated is a dataframe that converts to excel.

Things to consider, when changing users it depends on their role and profile within the platform since their url will depend on this and in turn the way to enter the transaction (frames).

Finally, in theory all possible SAP errors are mapped in such away that they doesn't have to be executed in a supervised way.

> *Note:* To be able to perform inspection in a scrollbar, was based on this following: https://twitter.com/sulco/status/1305841873945272321 

For install the chromedriver you have to search your chrome version and then download it here [Chrome Driver](https://chromedriver.chromium.org/downloads)

> Otherwise, the transaction downloads files that contain *export.xlsx* which are not taken into consideration when consolidating, so in the consolidation function these are eliminated.

## SQL
Install [ODBC](https://docs.microsoft.com/en-us/sql/connect/odbc/linux-mac/install-microsoft-odbc-driver-sql-server-macos?view=sql-server-ver15)

For insert database from python into SQL Server :
- [sql-insert-tutorial](https://www.dataquest.io/blog/sql-insert-tutorial/)
- [Retrieving Data from SQL Using pyodbc](https://stackoverflow.com/questions/11451101/retrieving-data-from-sql-using-pyodbc/11451863)
- [Bulk Insert A Pandas DataFrame Using SQLAlchemy](https://stackoverflow.com/questions/31997859/bulk-insert-a-pandas-dataframe-using-sqlalchemy)


## Execute locally
For execute this code you have to run some commands in this order: 
1. Open the folder on the terminal
2. Activate virtual enviroment
```bash
python3 -m venv env
source ./env/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Then you have to create a new file called `.env` who have the credentials. For example:
```env
user_name=YOUR USERNAME
password="YOUR PASSWORD"
driver_path="./chromedriver"
server_sql = "SERVER SQL"
database = "DATABASE"
user_sql = "USERNAME SQL"
pass_sql = "PASSWORD SQL"
mssql_driver = "ODBC+Driver+17+for+SQL+Server"
```