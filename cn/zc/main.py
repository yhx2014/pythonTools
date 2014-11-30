# -*- coding: utf8 -*-
'''
Created on 2014-11-24

@author: zhanghl
'''
import logging.config

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
        pass
    
if __name__ == "__main__":
    main().main()

