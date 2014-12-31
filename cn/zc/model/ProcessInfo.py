# -*- coding: utf8 -*-
'''
Created on 2014-11-24

@author: zhanghl
'''
import json
from cn.tools import Md5Tools

class ProcessInfo(object):
    '''
    classdocs
    '''
    
    def __init__(self,
                name = '',        #名称
                startTime = 0l,   #开始时间 秒
                endTime = 0l ,    #结束时间 秒
                useduration = 0l, #运行时长 秒
                count = 0,        #运行次数
                desc = ''        #描述
                ,status=False   #运行状态
                ,executablePath='' #运行文件路径
                 ):
        '''
        Constructor
        '''
        self.name = name
        self.startTime= startTime
        self.endTime = endTime
        self.useduration = useduration
        self.count= count
        self.desc= desc
        self.status= status
        self.executablePath = executablePath

    def __str__(self):
        return "name=%s,startTime=%d,endTime=%d,useduration=%d,count=%d,desc=%s,status=%s" %(self.name,self.startTime,self.endTime,self.useduration,self.count,self.desc,self.status)


class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        #convert object to a dict
        d = {}
        d['__class__'] = obj.__class__.__name__
        d['__module__'] = obj.__module__
        d.update(obj.__dict__)
        return d
 
class MyDecoder(json.JSONDecoder):
    def __init__(self):
        json.JSONDecoder.__init__(self,object_hook=self.dict2object)
    def dict2object(self,d):
        #convert dict to object
        if'__class__' in d:
            class_name = d.pop('__class__')
            module_name = d.pop('__module__')
            module = __import__(module_name)
            class_ = getattr(module,class_name)
            args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
            inst = class_(**args) #create new instance
        else:
            inst = d
        return inst
        
def object2dict(obj):
    #convert object to a dict
    d = {}
    d['__class__'] = obj.__class__.__name__
    d['__module__'] = obj.__module__
    d.update(obj.__dict__)
    return d
 
def dict2object(d):
    #convert dict to object
    if'__class__' in d:
        class_name = d.pop('__class__')
        module_name = d.pop('__module__')
        module = __import__(module_name)
        class_ = getattr(module,class_name)
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args
        inst = class_(**args) #create new instance
    else:
        inst = d
    return inst

class WindowInfo(object):
    def __init__(self,
                name = '',        #名称
                startTime = 0l,   #开始时间 秒
                endTime = 0l ,    #结束时间 秒
                useduration = 0l, #运行时长 秒
                count = 0,        #运行次数
                desc = ''        #描述
                ,executablePath='' #运行文件路径
                ,md5=''
                ,dt=''  #日期，为统计天数据用
                 ):
        self.name = name
        self.startTime= startTime
        self.endTime = endTime
        self.useduration = useduration
        self.count= count
        self.desc= desc
        self.executablePath = executablePath
        self.md5 = Md5Tools.getStrMd5(executablePath)
        self.dt = dt

# 
# p = ProcessInfo(name='adfa',startTime=1231)
# aa = {p.name:p}
# # print p.__dict__
# cc = MyEncoder().encode(aa)
# print cc
# 
# o = MyDecoder().decode(cc)
# 
# print type(o),o,o["adfa"]

