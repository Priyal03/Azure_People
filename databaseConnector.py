import pyodbc

server = 'tcp:pxp6118.database.windows.net,1433'
database = 'pxp6118database'
username = 'pxp6118'
password = 'October@1994'
driver = '{ODBC Driver 17 for SQL Server}'

try:
    connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    print('connection to database is successful')
except Exception as e:
	print(e)
	connect = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)