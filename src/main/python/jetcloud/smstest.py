'''
Created on 2015

@author: aadebuger
'''

import requests
import json
#Content-Type: application/json

def clientGet():
        url ="http://www.slowyou.com.cn:5010/1.1/requestMobilePhoneVerify"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"13906917736","password":"password"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text
def smscodeGet():
        url ="http://www.slowyou.com.cn:5010/1.1/verifyMobilePhone/600600"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"13906917736","password":"password"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text        
def loginGet():
        url ="http://192.168.1.9:8080/1.1/login"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"13906917736","password":"password"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text   
def smsCode():
        url ="http://yh.singfan.cn:5010/1.1/requestPasswordResetBySmsCode"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"18501372374"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text   
def resetPassword():
        url ="http://yh.singfan.cn:5010/1.1/resetPasswordBySmsCode/112233"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"password":"567890"})
        r = requests.put(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text   
def resetPasswordok():
        url ="http://yh.singfan.cn:5010/1.1/resetPasswordBySmsCode/437413"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"password":"437413"})
        r = requests.put(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text                         
if __name__ == '__main__':
             clientGet()
#             smscodeGet()
#            smsCode();
#            resetPasswordok();     