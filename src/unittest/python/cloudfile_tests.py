# -*- coding: utf-8 -*-
'''
Created on 2015年5月31日

@author: aadebuger
'''
import unittest
from jetcloud import cloudfile

class Test(unittest.TestCase):


    def testName(self):
         cloudfile.uploadfile("hello.txt","hello")
    def testJpg(self):
         data = cloudfile.get_bin_file('512-1.jpg')
         cloudfile.uploadfile("512-1.jpg", data)
         

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()