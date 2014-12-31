'''
Created on 2014-12-9

@author: zhanghl
'''
import MySQLdb
import sqlite3
class mysqlDB():
    def __init__(self):
        conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="test", charset="utf8") 
        self.__conn = conn
    
    def getConn(self):
        return self.__conn
        

class sqlliteDB():
    def __init__(self,path):
        conn = sqlite3.connect(path)
        self.__conn = conn
        pass
    
    def getConn(self):
        return self.__conn