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

    def testDelete(self):
        print 'users delete'
        rv=self.app.delete('/1.1/classes/users/5577c699421aa912020de9ad',headers={'X-AVOSCloud-Session-Token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNDI4NTE5NCwiaWF0IjoxNDMzOTI1MTk0fQ.IjU1NzdjNjk5NDIxYWE5MTIwMjBkZTlhZCI.xj4NORTV7FwHEpZlgjylay08YzsHVMzvS9VOea3CmNc'})
                
        print 'news rv=',rv
        print 'news rv=',rv.data     


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testDelete']
    unittest.main()