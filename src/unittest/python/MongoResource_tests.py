# -*- coding: utf-8 -*-
'''
Created on 2015年5月31日

@author: aadebuger
'''
import unittest
from jetcloud import MongoResource

class Test(unittest.TestCase):


    def testNewBucketUpload(self):
            ret=MongoResource.newBucketUpload("files",32,"testbucket","222.qiniu.com","hello.txt")
            print 'ret=',ret

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()