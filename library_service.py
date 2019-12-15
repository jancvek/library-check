import time
import datetime
import smtplib
from email.message import EmailMessage

import os

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, '/home/serverpc/jan-projects/jan_lib')
import jan_cobiss
import jan_email
import jan_enum
import jan_sqlite

currPath = os.path.dirname(os.path.abspath(__file__))
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
    values1 = '1,'+str(cobissJan.status)+','+cobissJan.error
    print(values1)
    jan_sqlite.insert_data(sqlConn, 'data', ("created_by_service", "status", "text"),values1)

if(cobissJan.isError):
    print(cobissJan.error)
    email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - ERROR!','Error Knjiznica Jan: '+cobissJan.error)
else:
    if cobissJan.status == jan_enum.EStatusLibrary.EXPIRE_SOON:
        email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - VRNI!','Knjiznica Jan se: '+cobissJan.minDays+' dni do preteka!')

    print(str(cobissJan.minDays))
    print(str(cobissJan.status))


cobissMasa = jan_cobiss.Cobiss("0107170","knjiga")
cobissMasa.checkCobiss()

with sqlConn:
    values2 = '1,'+str(cobissMasa.status)+','+cobissMasa.error
    jan_sqlite.insert_data(sqlConn, 'data', ("created_by_service", "status", "text"),values2)

if(cobissMasa.isError):
    print(cobissMasa.error)
    email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - ERROR!','Error Knjiznica Masa: '+cobissMasa.error)
else:
    if cobissJan.status == jan_enum.EStatusLibrary.EXPIRE_SOON:
        email.sentEmail(['jan.cvek@gmail.com'],'Knjiznica API - VRNI!','Knjiznica Masa se: '+cobissMasa.minDays+' dni do preteka!')

    print(str(cobissMasa.minDays))
    print(str(cobissMasa.status))

