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
        rv=self.app.get('/1.1/yhorder')
                
        print 'yhorder rv=',rv
        print 'yhorder rv=',rv.data  
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()