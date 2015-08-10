'''
Created on Aug 2, 2015

@author: aadebuger
'''
import unittest
from mongoengine import *
from jetcloud import jetcloudrest
from jetcloud import util
from pymongo import read_preferences


class Test(unittest.TestCase):

    
    def setUp(self):
        connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
        self.app = jetcloudrest.app.test_client()


    def tearDown(self):
        pass
    

    def testYhorderlist(self):
        print 'get yhorder'
        jetcloudrest.yhRoute()
        rv=self.app.get('/1.1/classes/yhorder')
                
        print 'yhorder rv=',rv
        print 'yhorder rv=',rv.data  
        
    def testYhorderlistbyheader(self):
        print 'get yhorder by header '
        rv=self.app.get('/1.1/classes/yhorder',headers={'X-AVOSCloud-Session-Token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ0MjI3NTk1MCwiaWF0IjoxNDM4Njc1OTUwfQ.IjU1YWU2YjBhNDIxYWE5MDRjZDIzYTgwOCI.cMBo0Za7L8WXKST9PwyJFWzWr3Hr52YGtREAg9dhWok'})
                
        print 'yhorder rv=',rv
        print 'yhorder rv=',rv.data  
    def testYhorderlistbyheaderok(self):
        print 'get yhorder by header ok'
        rv=self.app.get('/1.1/classes/yhorder',headers={'X-AVOSCloud-Session-Token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNDI4NTE5NCwiaWF0IjoxNDMzOTI1MTk0fQ.IjU1NzdjNjk5NDIxYWE5MTIwMjBkZTlhZCI.xj4NORTV7FwHEpZlgjylay08YzsHVMzvS9VOea3CmNc'})
                
        print 'yhorder rv=',rv
        print 'yhorder rv=',rv.data  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()