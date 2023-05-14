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

def execSQL(conn, sqlFile, additionalTuple=()):
    sql = parseSQL(sqlFile)
    c = conn.cursor()
    for code in sql:
        if additionalTuple != ():
            c.execute(code)
        else:
            c.execute(code,additionalTuple)
    conn.commit()
def execSelect(conn,sqlFile,term):
    sql = parseSQL(sqlFile)
    c = conn.cursor()
    for code in sql:
        if term != '':
            c.execute(code,(term,))
        else:
            c.execute(code)
    return c.fetchall()
def execAddProfile(conn,details):
    sql = parseSQL("addProfile.txt")
    c = conn.cursor()
    for code in sql:
        c.execute(code.format(*tuple(details.values())))
    conn.commit()
    return(c.lastrowid)
def execUpdateProfile(conn,details):
    sql = parseSQL("updateProfile.txt")
    c = conn.cursor()
    for code in sql:
        code = code.format(*tuple(details))
        c.execute(code)
    conn.commit()
    return(c.lastrowid)