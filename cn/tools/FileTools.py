'''
Created on 2014-12-1

@author: zhanghl
'''
from cn.zc.model.ProcessInfo import MyDecoder, MyEncoder
import os

def saveToFile(data,fileName):
    try:
        msg = MyEncoder().encode(data)
        with open(fileName,'w') as f:
            f.write(msg)
            f.flush()
    finally:
        f.close()

def loadDataFromFile(fileName):
    result = {}
    f = None
    try:
        if os.path.exists(fileName):
            with open(fileName,'r') as f:
                msg = f.read()
                result = MyDecoder().decode(msg)
    finally:
        if f:
            f.close()
    return result


# fileName = "c:/test.dd"
# data = {"ad":123,"acc":WindowInfo(name="cda.exe",useduration=111)}
# saveToFile(data, fileName)
#  
# c = loadDataFromFile(fileName)
#   
# print c["acc"].name

