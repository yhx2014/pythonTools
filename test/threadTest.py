# -*- coding: utf8 -*-

'''
Created on 2014-11-27
 线程测试
@author: zhanghl
'''
import threading


class Thread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "test"
        
    def run(self):
        print "tst............"
        threading.Thread.run(self)


c = Thread1()
c.start()
print "线程开始测试了"