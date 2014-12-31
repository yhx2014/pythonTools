# -*- coding: utf8 -*-
'''
Created on 2014-12-9

@author: zhanghl
'''
from cn.tools import FileTools
from cn.tools.dbTools import sqlliteDB
from cn.zc.model.ProcessInfo import WindowInfo
import MySQLdb
import datetime
import json
class processDao():
    def __init__(self,db):
        self.db = db
        tableName ="window_info"
        
        if not self.isExist(tableName):
            self.createTable()
    
    def createTable(self):
        sql = "CREATE TABLE if not exists  `window_info`"
        sql += "( id integer PRIMARY KEY autoincrement"
        sql += ",name varchar(100) DEFAULT NULL"
        sql += ",md5 varchar(100) DEFAULT NULL"
        sql += ",useduration int DEFAULT 0"
        sql += ",count int DEFAULT 0"
        sql += ",`desc` varchar(400) DEFAULT NULL"
        sql += ",executablePath varchar(800) DEFAULT NULL"
        sql += ",dt date DEFAULT NULL"
        sql += ");"
        
        cursor = self.db.getConn()
        cursor.execute(sql)
        
    def isExist(self,tableName):
        '''
                 判断表是否存在
        '''
        result = False
        sql = "SELECT COUNT(*) FROM sqlite_master where type='table' and name=%s"
        conn = self.db.getConn()
        try:
            cursor = conn.cursor()
            n = cursor.execute(sql,(tableName))
            
            for row in cursor.fetchall():
                if row[0] > 0:
                    result = True
                    break
        finally:
            return result
     
    def saveData(self,processes={}):
        if processes:
            #先判断是否存在，存在，更新，不存在新增
            conn = self.db.getConn()
            cursor = conn.cursor()
            
            querySql = "select count(*) from window_info where md5=? and dt=?"
            
            insertSql = "insert into window_info (name,useduration,count,executablePath,md5,dt) values(?,?,?,?,?,?)"
                    
            updateSql = "update window_info set name=?,useduration=?,count=?,executablePath=? where md5=? and dt=?"
            for pro in processes:
                if pro.strip()!='':
                    model = processes.get(pro)
                    param = (model.md5,model.dt,)
                    count = cursor.execute(querySql,param)
                    
                    boo = True
                    for row in count:
                        boo = row[0]==0
                    
                    print boo
                    param2 =  (model.name,model.useduration,model.count,model.executablePath,model.md5,model.dt,)
                    if boo:
                        print "insert",cursor.execute(insertSql,param2)
                    else:
                        print "update",cursor.execute(updateSql,param2)
                        
            cursor.close()
            conn.commit()
       
    def insertData(self,processes={},dt = datetime.datetime.now().strftime("%Y-%m-%d")):
        if processes:
            insertSql = "insert into window_info"
            insertSql += " (name,useduration,count,md5,executablePath,dt)"
#             insertSql += "values(%s,%s,%s,%s,%s,%s,%s)";
            insertSql += "values(?,?,?,?,?,?)";
            conn = self.db.getConn()
            cursor = conn.cursor()
            for pro in processes:
                if pro.strip()!='':
                    model = processes.get(pro)
                    param = (model.name,model.useduration,model.count,model.md5,model.executablePath,dt,)
                    
                    print param,cursor.execute(insertSql,param)
            
            cursor.close()
            conn.commit()
    
class db():
    def __init__(self):
        conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8") 
        self.__conn = conn
    
    def getConn(self):
        return self.__conn

#         
# filePath = "c:/tmp"
# dbFile = filePath + "/sqlite2.db"
# db1 = sqlliteDB(dbFile)
# pdao = processDao(db1)
# fileName = filePath + "/windowInfo_20141229.json"
# result = FileTools.loadDataFromFile(fileName)
# pdao.saveData(result)

# conn= MySQLdb.connect(host="localhost",user="root",passwd="root",db="test",charset="utf8") 
# cursor = conn.cursor()
# sql = "select count(*) from window_info";
# n = cursor.execute(sql)
# for row in cursor.fetchall():
#     print row[0]

# aa = datetime.datetime.now().strftime("%Y-%m-%d")

# print aa

