'''
Created on 2015

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


    def testLoginok(self):
        print 'baber Login'
        rv=self.app.get('/1.1/login?username=13718019928&&password=88888888')
                
        print 'barber login rv=',rv
        print 'barber login  rv=',rv.data
    def testLoginfail(self):
        print 'baber Login'
        rv=self.app.get('/1.1/login?username=13718019928&&password=88888877')
                
        print 'barber login rv=',rv
        print 'barber login  rv=',rv.data
                


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()