# -*- coding: utf8 -*-
'''
Created on 2014-11-24

@author: zhanghl
'''
from cn.tools import FileTools
from cn.tools.dbTools import sqlliteDB
from cn.zc.dao.ProcessDao import processDao
from cn.zc.service.mywindow import hook, Watch
import datetime
import logging.config
import pythoncom
import threading
import win32api

class main():
    '''
    classdocs
    '''
    
    def __init__(self):
        '''
        Constructor
        '''
        logging.config.fileConfig("../../config/logging.cfg")
        logging.info("初始化.......")
        filePath = "c:/tmp"
        self.filePath = filePath
        dbFile = filePath + "/sqlite.db"
        db = sqlliteDB(dbFile)
        dao = processDao(db)
        self.dao = dao
    
    def main(self):
        filePath = self.filePath
        h = hook(filePath, toolsMain=self)
        self.hook =h
        
        w = Watch(filePath)
        self.process = w
        
        h.main()
        w.main()    
        self.doStop = threading.Thread(target=self.executeStop)
        loadData= threading.Thread(target=self.loadDataToDB)
        loadData.start()
        pythoncom.PumpMessages()
    def executeStop(self):
        if self.hook:
            self.hook.stop()
        if self.process:
            self.process.stop()
    def loadDataToDB(self):
        '''
        把数据放到数据库中
        '''
        yd = str(datetime.date.today() + datetime.timedelta(-1))
        fileName = self.filePath + "/windowInfo_" + yd + ".json"
        result = FileTools.loadDataFromFile(fileName)
        if result:
            self.dao.saveData(result)
#             self.dao.insertData(result,yd)
        pass
            
    def stop(self):
        self.doStop.start()
        win32api.PostQuitMessage()
        
if __name__ == "__main__":
    main().main()
    
    
    
# db = mysqlDB()
# db = sqlliteDB(path = "c:/tmp/pythontools_sqllite.db")
# 
# cu = db.getConn().cursor()
# a = db.getConn().execute("insert into window_info (name) values(?)",(u"11",))
# db.getConn().commit()
# print a 
# 
# 
# cu.execute("select * from window_info")
# print cu.fetchall()

# conn = db.getConn()
# cu=conn.cursor()
# cu.execute("create table catalog (id integer primary key,pid integer,name varchar(10) UNIQUE,nickname text NULL)")
#  
# dao = processDao(db)
# fileName = "c:/tmp/windowInfo_20141202.json"
# result = FileTools.loadDataFromFile(fileName)
# if result:
#     for r in result:
#         print r
# dao.insertData(processes=result,dt='2014-12-02')
# print result