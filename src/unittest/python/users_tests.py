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


    def testNewusers(self):
        print 'Newusers'
        rv=self.app.post('/api/users',data="""{"username":"zhuanghua","password":"password"}""",content_type="application/json")
                
        print 'news rv=',rv
        print 'news rv=',rv.data
    def testLoginfail(self):
        print 'Login'
        rv=self.app.get('/1.1/login?username=aa&&password=hello')
                
        print 'news rv=',rv
        print 'news rv=',rv.data
    def testLoginok(self):
        print 'Login'
        rv=self.app.get('/1.1/login?username=zhuanghua&&password=password')
                
        print 'news rv=',rv
        print 'news rv=',rv.data
    def testNewusers2(self):
        print 'Newusers'
        rv=self.app.post('/api/users',data="""{"username":"zhuanghua2","password":"password2"}""",content_type="application/json")
                
        print 'Newusers2 rv=',rv
        print 'Newusers2 rv=',rv.data
    def testNewusers3(self):
        print 'Newusers3'
        rv=self.app.post('/api/users',data="""{"username":"zhuanghua3","password":"password3"}""",content_type="application/json")
                
        print 'Newusers3 rv=',rv
        print 'Newusers3 rv=',rv.data
    def testGetusers(self):
        print 'get users'
        rv=self.app.get('/1.1/users/5577c699421aa912020de9ad')
                
        print 'Getusers rv=',rv
        print 'Getusers rv=',rv.data    
    def testVerifyMobilePhone(self):
        print 'verifyMobilePhone'
        rv=self.app.post('/1.1/verifyMobilePhone/123456',data="""""",content_type="application/json",
                         headers={'X-AVOSCloud-Session-Token': 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzNDI4NTE5NCwiaWF0IjoxNDMzOTI1MTk0fQ.IjU1NzdjNjk5NDIxYWE5MTIwMjBkZTlhZCI.xj4NORTV7FwHEpZlgjylay08YzsHVMzvS9VOea3CmNc'})
                
        print 'VerifyMobilePhone rv=',rv
        print 'VerifyMobilePhone rv=',rv.data     
    def testNewusers13906917736(self):
        print 'Newusers 13906917736'
        rv=self.app.post('/1.1/users',data="""{"username":"13906917736","password":"password2"}""",content_type="application/json")
                
        print 'Newusers2 rv=',rv
        print 'Newusers2 rv=',rv.data            

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()