# -*- coding: utf8 -*-
'''
Created on 2014-12-1
窗口运行监控
@author: zhanghl
'''
from cn.tools import FileTools, Md5Tools
from cn.zc.model.ProcessInfo import WindowInfo, MyEncoder, MyDecoder, \
    ProcessInfo
import logging
import os
import psutil
import pyHook
import pythoncom
import threading
import time
import win32gui
import win32process
import wmi

windowInfo = WindowInfo()
allInfos = {}

class hook(object):
    
    def __init__(self,
                 filePath = "c:/tmp",toolsMain =None):

        dayTime = time.strftime("%Y%m%d");
        self.dayTime = time.strftime("%Y-%m-%d");
        fileName = filePath + "/windowInfo_" + dayTime + ".json"
        self.fileName = fileName
        self.toolsMain = toolsMain
        self.__loadData(self.fileName)
        self.status = True
    
    def __loadData(self,fileName):
        global allInfos
        allInfos = FileTools.loadDataFromFile(fileName)

    def stop(self):
        self.status = False
    
    def onKeyboardEvent(self,event):
        '''
            监控监控
        '''
        if str(event.Key) == 'F12':  # 按下F12后终止
            print "stop....."
            self.toolsMain.stop()
            return False
#             win32api.PostQuitMessage()
#             self.status = False
        else:
            pass
        self.doEventExecute(event.Window)
        return True
    
    def onMouseEvent(self,event):
        '''
            鼠标监控
        ''' 
        self.doEventExecute(event.Window)
        return True

    def getPidByWindow(self,window=0):
        if win32gui.IsWindowVisible (window) and win32gui.IsWindowEnabled (window):
            _, found_pid = win32process.GetWindowThreadProcessId (window)
            return found_pid 
        else:
            return 0
         
    def doEventExecute(self,window):
        global windowInfo,allInfos 
        t = windowInfo.md5
        pid = self.getPidByWindow(window)
        p = psutil.Process(pid)
        exeStr = p.exe()
        exeName = p.name()
        pName = Md5Tools.getStrMd5(exeStr)
        if t==pName:
            pass
        else:
            #切换当前窗口
            currentTime = time.time()
            if windowInfo.executablePath!='':
                useTime = currentTime - windowInfo.startTime
                windowInfo.useduration = windowInfo.useduration + useTime
                windowInfo.dt = self.dayTime
                #记录上次窗口使用时间
                allInfos[windowInfo.md5] = windowInfo

            if allInfos.has_key(pName):
                windowInfo = allInfos.get(pName)
                windowInfo.startTime = time.time()
                windowInfo.count = windowInfo.count+1
            else:
                windowInfo = WindowInfo(name=exeName,startTime=currentTime,md5=pName,executablePath=exeStr)
                
    def saveDataToFile(self):
        global allInfos
        while True & self.status:
            time.sleep(60)
            FileTools.saveToFile(allInfos, self.fileName)
            
        
    def main(self):
        global allInfos
        hm = pyHook.HookManager()  
        
    # 监控键盘  
        hm.KeyDown = self.onKeyboardEvent
        hm.HookKeyboard()  

# MouseMove = property(fset=SubscribeMouseMove)
#   MouseLeftUp = property(fset=SubscribeMouseLeftUp)
#   MouseLeftDown = property(fset=SubscribeMouseLeftDown)
#   MouseLeftDbl = property(fset=SubscribeMouseLeftDbl)
#   MouseRightUp = property(fset=SubscribeMouseRightUp)
#   MouseRightDown
        hm.MouseLeftDown = self.onMouseEvent
        hm.MouseRightDown = self.onMouseEvent
        hm.MouseWheel = self.onMouseEvent
        hm.HookMouse()
        
        threading.Thread(target=self.saveDataToFile).start()
        

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
        self.status = True
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
        while self.status:
            time.sleep(60)
            msg = self.jsonEncode.encode(self.processInfo)
            with open(self.fileName,'w') as f:
                f.write(msg)
                f.flush()
    
    def stop(self):
        self.status = False
        self.thread1.stop()
        self.thread2.stop()
    
    def main(self):
        t = threadWatch(self.watch_creation,self)
        t.start()
        t2 = threadWatch(self.watch_deletion,self)
        t2.start()
        
        self.thread1 = t
        self.thread2 = t2
        threading.Thread(target=self.saveFile).start()
        print "process watch start.............."
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
        logging.info(self.name + " thread status")
        self.thread_stop = True
 
    
if __name__ == "__main__2":
    Watch().main()
    hook().main()
    pythoncom.PumpMessages()

