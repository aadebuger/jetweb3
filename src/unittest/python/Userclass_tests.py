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


    def testName(self):
            oid="5577c699421aa912020de9ad"
            user= jetcloudrest.User.objects(pk=oid).first()
            print 'user=',user
            print 'user username',user.username
            print 'user smscode=',user.smscode
            user.build_smscode();
            print 'user smscode=',user.smscode  
    def testVerify_auth_token(self):
            print "Verify_auth_token"
            user = jetcloudrest.User.verify_auth_token("eyJhbGciOiJIUzI1NiIsImV4cCI6MTQzMzkyNTM5OSwiaWF0IjoxNDMzOTI0Nzk5fQ.IjU1NzdjNjk5NDIxYWE5MTIwMjBkZTlhZCI.g7QDJfgUTT_hLVrtXba8j2GCj_uJ962UithrSC7bKg4")       
            print 'user=',user
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()