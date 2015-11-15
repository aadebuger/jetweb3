# -*- coding: utf-8 -*-
'''
Created on Aug 5, 2015

@author: aadebuger
'''
import requests
import json
import urllib
from  urllib  import unquote
def hlquicksend(phone,smscode):
    
        message = "您的验证码是：%s。请不要把验证码泄露给其他人。"%(smscode)

        payload = {'linkid':'','subcode':'','username':'zrxt','password':'password777','epid':'109430','phone':phone,'message':urllib.quote_plus(message.decode("utf-8").encode("gb2312"))}

        ret =requests.get('http://114.255.71.158:8061',params=payload)
        print 'ret=',ret.text
        
if __name__ == '__main__':
     hlquicksend("13906917736","hello")