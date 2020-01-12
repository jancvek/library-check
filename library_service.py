import time
import datetime
import smtplib
from email.message import EmailMessage

import os

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)
import jan_cobiss
import jan_email
import jan_enum
import jan_sqlite

def checkLibrary():

    sqlConn = jan_sqlite.create_connection(currPath+"/library.db")

    print(currPath+"/library.db")

    email = jan_email.Email()

    cobissJan = jan_cobiss.Cobiss("0104232","knjiga")
    cobissJan.checkCobiss()

    if sqlConn:
        print("sqlConn dela")
    else:
        print("sqlConn ne dela!")

    with sqlConn:
        params1 = "created_by_service,library_user,status,days_to_expire,text"
        values1 = ('1','JAN',str(cobissJan.status.name),cobissJan.minDays,cobissJan.error)   
        jan_sqlite.insert_data(sqlConn, 'data', params1, values1)

    if cobissJan.isError:
        print(cobissJan.error)
        email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - ERROR!','Error Knjiznica Jan: '+cobissJan.error)
    else:
        if cobissJan.status == jan_enum.EStatusLibrary.EXPIRE_SOON:
            email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - VRNI!','Knjiznica Jan se: '+str(cobissJan.minDays)+' dni do preteka!')

        print(str(cobissJan.minDays))
        print(str(cobissJan.status))


    cobissMasa = jan_cobiss.Cobiss("0107170","knjiga")
    cobissMasa.checkCobiss()

    with sqlConn:
        params2 = "created_by_service,library_user,status,days_to_expire,text"
        values2 = ('1','MASA',str(cobissMasa.status.name),cobissMasa.minDays,cobissMasa.error)  
        jan_sqlite.insert_data(sqlConn, 'data', params2, values2)

    if cobissMasa.isError:
        print(cobissMasa.error)
        email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - ERROR!','Error Knjiznica Masa: '+cobissMasa.error)
    else:
        if cobissMasa.status == jan_enum.EStatusLibrary.EXPIRE_SOON:
            email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - VRNI!','Knjiznica Masa se: '+str(cobissMasa.minDays)+' dni do preteka!')

        print(str(cobissMasa.minDays))
        print(str(cobissMasa.status))

# tole se zazene ko je to main program ni klican iz druge kode
if __name__ == '__main__':
   checkLibrary()