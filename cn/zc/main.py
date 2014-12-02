# -*- coding: utf8 -*-
'''
Created on 2014-11-24

@author: zhanghl
'''
from cn.zc.service.mywindow import hook, Watch
import logging.config
import pythoncom
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
        
        pythoncom.PumpMessages()
    def stop(self):
        if self.hook:
            self.hook.stop()
        if self.process:
            self.process.stop()
        win32api.PostQuitMessage()
        
if __name__ == "__main__":
    main().main()

