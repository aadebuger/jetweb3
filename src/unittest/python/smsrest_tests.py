# -*- coding: utf-8 -*-
'''
Created on Jul 21, 2015

@author: aadebuger
'''
import unittest
from jetcloud import smsrest

class Test(unittest.TestCase):


    def testName(self):
        xml="""<?xml version="1.0" encoding="utf-8"?>
<SubmitResult xmlns="http://106.ihuyi.cn/">
<code>2</code>
<msg>提交成功</msg>
<smsid>116326079</smsid>
</SubmitResult>"""
        xml="""<?xml version="1.0" encoding="utf-8"?>
<SubmitResult xmlns="http://106.ihuyi.cn/">
<code>4085</code>
<msg>验证码短信每天每个手机号码只能发5条</msg>
<smsid>0</smsid>
</SubmitResult>"""
        smsrest.parseQuicksendxml(xml)
    def testName1(self):
        xml="""<?xml version="1.0" encoding="utf-8"?>
<SubmitResult xmlns="http://106.ihuyi.cn/">
<code>2</code>
<msg>提交成功</msg>
<smsid>116326079</smsid>
</SubmitResult>"""
  
        smsrest.parseQuicksendxml(xml)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()