# -*- coding: utf-8 -*-
'''
Created on 2014年8月5日

@author: aadebuger
'''

import os

def getMydbip():
    return os.environ.get('MYDB_PORT_27017_TCP_ADDR',"127.0.0.1")

if __name__ == '__main__':
    pass