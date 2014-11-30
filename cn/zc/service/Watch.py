# -*- coding: utf8 -*-

'''
Created on 2014-11-24

@author: zhanghl
'''
from cn.zc.model.ProcessInfo import ProcessInfo, MyEncoder, \
    MyDecoder
import logging
import os.path
import pythoncom
import threading
import time
import wmi

class Watch(object):
    '''
    classdocs
    '''
    def __init__(self
                 ,filePath="c:/tmp"):
        '''
        Constructor
        '''
        self.log = logging.getLogger("root")
        self.log.info("监控 init")
        self.watch_creation = 'creation'
        self.watch_deletion = 'deletion'
        self.processInfo = {}
        self.filePath = filePath
        self.blackList = []
        self.wmi = wmi.WMI()
        self.jsonEncode = MyEncoder();
        self.jsonDecode = MyDecoder();
        
        dayTime = time.strftime("%Y%m%d");
        fileName = filePath + "/processInfo_" + dayTime + ".json"
        self.fileName = fileName
        
        self.__loadData(fileName)
        
        #黑名单
        blackListFile = filePath + "/processInfo_blackList.json"
        if os.path.exists(blackListFile):
            with open(fileName,'r') as f:
                msg = f.read()
                self.blackList = self.jsonDecode.decode(msg);
    
    def __loadData(self,fileName):
        '''
            加载数据
        '''
        if os.path.exists(fileName):
            with open(fileName,'r') as f:
                msg = f.read()
                self.processInfo = self.jsonDecode.decode(msg);
    
    def startWatch_creation(self):
        self.log.info("监控creation开始")
        wathch1 = threadWatch(self.watch_creation,self)
        wathch1.start()
        
    
    def startWatch_deletion(self):
        self.log.info("监控deletion 开始")
        wathch1 = threadWatch(self.watch_deletion,self)
        wathch1.start()
        
    def processCreate(self,name,time,process):
        print "create.....",name
#         print process.__dict__
#         print process.Name,process.ProcessId
        
        if self.processInfo.has_key(name):
            #存在，判断
            processModel = self.processInfo.get(name)
            if processModel.status:
                #进程中还有，不用管
                return True
            else:
                #进程中没有
                processModel.startTime = time
                processModel.endTime = 0
                processModel.count = processModel.count + 1
                processModel.status = True
                processModel.executablePath = process.ExecutablePath
                self.processInfo[name] = processModel
                print "creation=",processModel
                return True
        else:
            pass
        
        #添加到processInfo 中
        p = ProcessInfo(name=name,startTime=time,status=True,executablePath=process.ExecutablePath)
        self.processInfo[name] = p
        print "creation=",p
#         self.log.info("process creation 添加......")
        
    def processDel(self,name,time,process):
#         print "deletion.....",name
        if self.processInfo.has_key(name):
            #存在，判断
            processModel = self.processInfo.get(name)
            if processModel.status:
                if self.isRun(name) == False:
                    #同一个exe 有多个进程，会同时停止
                    #进程中没有了，添加结束时间，add 运行次数,add 总运行时长
                    processModel.endTime = time
                    processModel.useduration = processModel.useduration + (processModel.endTime - processModel.startTime)
                    processModel.status = False
                    self.processInfo[name] = processModel
                    print "deletion=",processModel
        else:
            return True
    
    def doProcess(self,name='',process='',optType='',time=0):
        self.log.info("doProcess......")
        
        if name in self.blackList:
            return True
        
        if optType == self.watch_creation:
            self.processCreate(name, time, process)
        elif optType == self.watch_deletion:
            self.processDel(name, time, process)

    #查看进程是否运行，根据self.name
    def isRun(self,name):
        result = True
        try:
            pythoncom.CoInitialize()
            processes = wmi.WMI().Win32_Process (name=name)
            if processes:
                result = True
            else:
                result = False    
        finally:
            pythoncom.CoUninitialize ()
        return result
    
    #保存到文件中，按天
    def saveFile(self):
        msg = self.jsonEncode.encode(self.processInfo)
        with open(self.fileName,'w') as f:
            f.write(msg)
            f.flush()
#监控线程
class threadWatch(threading.Thread):

    def __init__(self,name,watch):
        threading.Thread.__init__(self)
        
        logging.info(name + "..init...")
        self._name = name
        self.thread_stop = False
        self.win32process = wmi.WMI().Win32_process
        self.watch = watch
        
        
    def run(self):
        try:
#             pythoncom.CoInitializeEx(0)
            pythoncom.CoInitialize()
            watcher1 = wmi.WMI().Win32_Process.watch_for(self._name)
            print "[%s]thread run............" %(self._name)
            while not self.thread_stop:
                process = watcher1()
                name = process.Caption
                self.watch.doProcess(name=name,process=process,optType=self._name,time=time.time())
        finally:
            pythoncom.CoUninitialize ()
            
    def stop(self):
        logging.info(self.name + " thread stop")
        self.thread_stop = True

watch = Watch()
t = threadWatch("creation",watch)
t.start()
t2 = threadWatch("deletion",watch)
t2.start()


while True:
    time.sleep(60)
    watch.saveFile()

print "start.............."

# wmi = wmi.WMI()
# wathc1 = wmi.Win32_Process.watch_for('creation')
# while True:
#     process = wathc1()
#     print process.Caption
pythoncom.PumpMessages()