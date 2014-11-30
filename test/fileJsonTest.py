'''
Created on 2014-11-28

@author: zhanghl
'''
import json

class fileUtil:
    
    def printJSON(self,data):
        msg = json.dumps(data);
        print msg
        return msg
        

    def saveFile(self,msg,fileName):
        with open(fileName,'w') as f:
            f.write(msg)
            f.flush()
            
    def readFile(self,fileName):
        with open(fileName,'r') as f:
            msg = f.read()
            print msg
            return msg
        pass
    
if __name__ == '__main__':
    pass

# ftest= fileUtil()
# 
# jsonD = {"a":"a","name":"test11111111","age":12}
# 
# ftest.printJSON({"a":"12312","123":123})
# 
# tmpFileName = "c:/tmp/tes.json"
# ftest.saveFile(ftest.printJSON(jsonD), tmpFileName)
# jsonStr = ftest.readFile(tmpFileName)
fileName = "C:/tmp/20141129.json"
with open(fileName,'r') as p:
    pass

