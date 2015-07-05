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
#        connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
        self.app = jetcloudrest.app.test_client()


    def tearDown(self):
        pass


    def testNewcollection(self):
        print 'Newcollection'
        rv=self.app.post('/1.1/classes/collection',data="""{"mycollection":"zhuanghua2"}""",content_type="application/json")
                
        print 'Newcollection rv=',rv
        print 'Newcollection rv=',rv.data


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()