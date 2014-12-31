
'''
Created on 2014-12-9

@author: zhanghl
'''

import hashlib

def getStrMd5(src):
    return hashlib.md5(src).hexdigest().upper()
