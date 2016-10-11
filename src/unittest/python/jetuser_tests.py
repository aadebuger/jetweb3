'''
Created on Oct 11, 2016

@author: aadebuger
'''
import unittest
import time
from jetcloud import jetuser
class Test(unittest.TestCase):


    def testName(self):
            user1 =jetuser.User.querybyauthData("weixin","0395BA18A5CD6255E5BA185E7BEBA242")
            print("authData user1",user1)
    def testNewUser(self):
                        user = jetuser.User(username="LeanCloud")
                        user.authData={  
    "weixin": {
      "openid": "0395BA18A5CD6255E5BA185E7BEBA242",
      "access_token": "12345678-SaMpLeTuo3m2avZxh5cjJmIrAfx4ZYyamdofM7IjU",
      "expires_in": 1382686496
    }
  }

                        user.password="123456"
                        user.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
                        user.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            
                                
                        user.save()
                        
                        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()