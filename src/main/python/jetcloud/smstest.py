# -*- coding: utf-8 -*-
'''
Created on 2015

@author: aadebuger
'''

import requests
import json
from  urllib  import unquote
#Content-Type: application/json
from smsrest import quicksend

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
def searchShop():
        url = 'http://yh.singfan.cn/1.1/classes/shop?limit=10&skip=0&where=%7B"location"%3A%7B"%24nearSphere"%3A%7B"__type"%3A"GeoPoint"%2C"latitude"%3A39.9087144%2C"longitude"%3A116.397389%7D%7D%2C"tags"%3A%7B"%24in"%3A%5B"吉米"%5D%7D%7D'
        print 'url=',unquote(url)
#        url ="http://yh.singfan.cn:5010/1.1/shop?where"
#        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
#        payload = json.dumps({"password":"437413"})
#        r = requests.put(url,data=payload,headers={'content-type': 'application/json'})
#        print 'r=',r.text 
def clientsmswebGet():
        url ="http://www.slowyou.com.cn:5030/1.1/requestMobilePhoneVerify"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"13906917736","password":"password"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text    

def smscodesmswebGet():
        url ="http://www.slowyou.com.cn:5030/1.1/verifyMobilePhone/423542"
        payload = """{"mobilePhoneNumber":"13906917736","password":"password"}"""
        payload = json.dumps({"mobilePhoneNumber":"13906917736","password":"password"})
        r = requests.post(url,data=payload,headers={'content-type': 'application/json'})
        print 'r=',r.text         
if __name__ == '__main__':
#        smscodesmswebGet()
         quicksend("13906917736","12345") 
#             clientsmswebGet()
#             searchShop()
#             smscodeGet()
#            smsCode();
#            resetPasswordok();     