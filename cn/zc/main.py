# -*- coding: utf8 -*-
'''
Created on 2014-11-24

@author: zhanghl
'''
from cn.zc.service.mywindow import hook, Watch
import logging.config
import pythoncom
import threading
import time
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
    
    def main(self):
        filePath = "c:/tmp"
        
        h = hook(filePath, toolsMain=self)
        self.hook =h
        
        w = Watch(filePath)
        self.process = w
        
        h.main()
        w.main()    
        self.doStop = threading.Thread(target=self.executeStop)

        pythoncom.PumpMessages()
    def executeStop(self):
        if self.hook:
            self.hook.stop()
        if self.process:
            self.process.stop()
    def stop(self):
        self.doStop.start()
        win32api.PostQuitMessage()
        
if __name__ == "__main__":
    main().main()

