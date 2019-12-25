import json
import os

currPath = os.path.dirname(os.path.abspath(__file__))
parentPath = os.path.dirname(currPath)
libPath = parentPath+'/jan-lib'

# tole moramo dodati da lahko importamo py file iz drugih lokacij
import sys
sys.path.insert(1, libPath)

import jan_sqlite


def getLibraryMain():

    sqlConn = jan_sqlite.create_connection(currPath+"/library.db")

    with sqlConn:
        # data = jan_sqlite.get_data_all(sqlConn,'data')
        data = jan_sqlite.run_query(sqlConn, "SELECT * FROM data ORDER BY created_on DESC LIMIT 30")
        

    dataList = []
    lastCheck = None
    latestJanDays = None
    latestMasaDays = None    
    for a in data:
        if lastCheck == None:
            lastCheck = a[1]
        if latestJanDays == None and a[3] == 'JAN':
            latestJanDays = a[5]
        if latestMasaDays == None and a[3] == 'MASA':
            latestMasaDays = a[5]

        d = {"id": a[0], "date": a[1], "user": a[3], "state": a[4], "min_days": a[5]}
        dataList.append(d)

    returnObj = {
        "minDays_jan": latestJanDays,
        "minDays_masa":latestMasaDays,
        "last_updated": lastCheck,
        "data": dataList
    }

    dJson = json.dumps(returnObj)

    print(dJson)

    return dJson
