import pymssql
import json

conn = pymssql.connect(server='pxp6118.database.windows.net',user='pxp6118@pxp6118', password='October@1994', database='pxp6118database')
cursor = conn.cursor()

def getCursor():
    return cursor

def readAllUsers():
#    cursor.execute('SELECT * from people;')
#    row = cursor.fetchone()
#    while row:
 #       print(str(row[0]) + " " + str(row[1]) + " " + str(row[2]) +
  #        " " + str(row[3]) + " " + str(row[4]) + " " + str(row[5]))
   #     row = cursor.fetchone()
    
    sql = "SELECT * from people"
    
    cursor.execute(sql)
    allusers = cursor.fetchall()

    #thislist = (list(allusers))  

    #for i in range(len(thislist)):
        #print(thislist[i])

    print("from database for Query= "+str(sql)+"; The response is : ")
    print(json.dumps(allusers))
    return allusers
    
    # =readAllUsers()
    # userlist=[]

    
def getPicbyName(username):
    cursor.execute('SELECT picture FROM people WHERE Name = %s', (username,))
    retu = cursor.fetchone()
    return str(retu)

