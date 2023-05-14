import sqlite3, os, csv
from sqlite3 import Error

def getConnection(dbFile): #get connection to the database file
    try:
        conn = sqlite3.connect(dbFile)
        print("DB Connected;",sqlite3.version)
        return conn
    except Error as e:
        print("getconnection:",e)

def define_path(file):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, file)
    return file_path

def parseSQL(file):
    file_path = define_path(file)
    f = open(file_path)
    full = f.read()
    sql_list = full.split(';')
    return sql_list

def execSQL(conn, sqlFile):
    sql = parseSQL(sqlFile)
    c = conn.cursor()
    for code in sql:
        c.execute(code)
    conn.commit()

def importOld(oldFile):
    print("Import: CSV Read (may take a while...)")
    with open(oldFile) as file:
        f = csv.reader(file,delimiter=',',quotechar='"')
        parks = []
        features = []
        file.readline()
        for tempEntries in f:
            parks.append({"parkID":tempEntries[0],"name":tempEntries[1],"long":float(tempEntries[11]),"lat":float(tempEntries[12])})
            features.append({"parkID":tempEntries[0],"featureID":tempEntries[5].translate({ord(c): None for c in ','}),"type":tempEntries[6],"name":tempEntries[7],"description":tempEntries[8]})
        file.close()
    
    print("Import: Parks reconfigration")
    dLast = ""
    known = []
    cI = 0 #current index
    dupeIndexes = []
    for d in parks: #trim duplicates
        if d["parkID"] == dLast or d["parkID"] in known:
            dupeIndexes.append(cI)
        else:
            known.append(dLast)
            dLast = d["parkID"]
        cI += 1
    for i in range(len(dupeIndexes)): #adjust indexes for changing due to popping
        dupeIndexes[i] = dupeIndexes[i] - i
    for i in dupeIndexes: #actually remove values from list
        parks.pop(i)
    
    print("Import: Feature reconfiguration")

    outFeatures = [] #restructure features system to fit db structure
    for fe in features:
        if fe["description"] != "":
            outFeatures.append({"parkID":fe["parkID"],"featureID":fe["featureID"],"data":fe["description"],"dataType":"d"})
        elif fe["name"] != "":
            outFeatures.append({"parkID":fe["parkID"],"featureID":fe["featureID"],"data":fe["name"],"dataType":"n"})
        else:
            outFeatures.append({"parkID":fe["parkID"],"featureID":fe["featureID"],"data":fe["type"],"dataType":"t"})
    print("Import: CSV import complete!")
    return parks, outFeatures

def fullImportOld(file, conn):
    csvImport = importOld(file)
    insertCode = parseSQL("insertData.txt")
    parks = csvImport[0]
    feats = csvImport[1]
    c = conn.cursor()
    for p in parks:
        try:
            c.execute(insertCode[0],tuple(p.values()))
        except Error as e:
            print("Import:",e,";",p["parkID"])
    for fe in feats:
        try:
            c.execute(insertCode[1],tuple(fe.values()))
        except Error as e:
            print("Import:",e,";",fe["featureID"])
    conn.commit()
    print("Full Old Import Complete;",c.lastrowid)

def exportNew(filename, conn):
    #get data from db
    exportSQL = parseSQL("exportTables.txt")
    c = conn.cursor()
    c.execute(exportSQL[0])
    parks = c.fetchall()
    c.execute(exportSQL[1])
    features = c.fetchall()
    c.execute(exportSQL[2])
    savedParks = c.fetchall()
    c.execute(exportSQL[3])
    users = c.fetchall()

    with open(define_path(filename),"w",newline='') as f:
        wr = csv.writer(f)
        writeList = []
        for p in parks:
            toWrite = ("parks",) + p
            writeList.append(toWrite)
        for fe in features:
            toWrite = ("features",) + fe
            writeList.append(toWrite)
        for s in savedParks:
            toWrite = ("savedParks",) + s
            writeList.append(toWrite)
        for u in users:
            toWrite = ("users",) + u
            writeList.append(toWrite)
        wr.writerows(writeList)

def importNew(filename, conn):
    print("Import: Importing new data structure")
    insertSQL = parseSQL("insertData.txt")
    sqlBindings = {"parks":0,"features":1,"savedParks":2,"users":3}
    with open(filename) as file:
        f = csv.reader(file,delimiter=',',quotechar='"')
        data = []
        for tempEntries in f:
            data.append(tempEntries)
    c = conn.cursor()
    for t in data:
        op = insertSQL[sqlBindings[t[0]]]
        t.pop(0)
        c.execute(op, tuple(t))
    conn.commit()
    print("Import: NI complete")

def checkAccountExists(conn, username, password, mode="login"):
    code = parseSQL("exportTables.txt")[3] #userID, username, password, type
    c = conn.cursor()
    c.execute(code)
    users = c.fetchall()
    userExists = False
    passCorrect = False
    accountType = "normal"
    id = False
    for u in users:
        if username.lower() == u[1].lower():
            userExists = True
            if password == u[2]:
                passCorrect = True
                accountType = u[3]
                id = u[0]
    if mode == "login":
        return(userExists, passCorrect, accountType, id)
    else:
        return(userExists)

def getIDs(conn):
    code = parseSQL("exportTables.txt")[3]
    c= conn.cursor()
    c.execute(code)
    users = c.fetchall()
    ids = []
    for u in users:
        ids.append(u[0])
    return ids
def enterData(conn, table, data):
    insertSQL = parseSQL("insertData.txt")
    sqlBindings = {"parks":0,"features":1,"savedParks":2,"users":3}
    c = conn.cursor()
    c.execute(insertSQL[sqlBindings[table]], data)
    conn.commit()
    print("DB updated:",c.lastrowid)

def getSearched(conn, term):
    code = parseSQL("selectSearched.txt")[0]
    c= conn.cursor()
    c.execute(code, (term,))
    parks = c.fetchall()
    return parks
def savePark(conn, id, user, saveBool):
    sql = parseSQL("editSaved.txt") #1 for delete, 0 for save
    c = conn.cursor()
    if saveBool == True:
        c.execute(sql[1].format(id,user))
        print("Park Unsaved")
    else:
        c.execute(sql[0], (id, user))
        print("Park Saved;",c.lastrowid)
    conn.commit()
def checkSaved(conn, id, user):
    sql = parseSQL("checkSaved.txt")[0]
    c = conn.cursor()
    c.execute(sql.format(id,user))
    result = c.fetchall()
    if result == []:
        return False
    else:
        return True
def getSaved(conn,userID):
    sql = parseSQL("getSaved.txt") # 0 is get ids from savedParks, 1 is get names from parks (could be a subquery instead)
    c = conn.cursor()
    c.execute(sql[0], (userID,))
    temp = list(c.fetchall())
    savedList = []
    for t in temp:
        savedList.append(t[0])
    names = []
    for id in savedList: #get park names to display
        c.execute(sql[1],(id,))
        names.append(c.fetchall()[0])
    output = []
    for i in range(len(savedList)): #put id and name of park in an array to turn into buttons
        output.append([savedList[i],names[i][0]])
    return output

def getDetails(conn,parkID):
    sql = parseSQL("getDetails.txt") #index 0 for long/lat, 1 for features(data,dataType)
    c = conn.cursor()
    c.execute(sql[0],(parkID,))
    latlongname =c.fetchall()
    c.execute(sql[1],(parkID,))
    feat = c.fetchall()
    output = {"name":latlongname[0][2],"long":latlongname[0][1],"lat":latlongname[0][0],"features":list(feat)}
    return output

def getAdminData(conn,table:str):
    link = {"parks":0,"features":1,"savedParks":2,"users":3}
    sql = parseSQL("exportTables.txt")
    c = conn.cursor()
    c.execute(sql[link[table]])
    fetch = c.fetchall()
    out = []
    for row in fetch:
        if table == "parks":
            out.append({"table":table,"parkID":row[0],"name":row[1],"long":row[2],"lat":row[3]})
        elif table == "features":
            out.append({"table":table,"parkID":row[0],"featureID":row[1],"data":row[2],"dataType":row[3]})
        elif table == "savedParks":
            out.append({"table":table,"parkID":row[0],"userID":row[1]})
        elif table == "users":
            out.append({"table":table,"userID":row[0],"username":row[1],"password":row[2],"type":row[3]})
    return(out)