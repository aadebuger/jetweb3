# -*- coding: utf-8 -*-
'''
Created on 2015

@author: aadebuger
'''

import sys
from flask import Flask
from flask import abort,jsonify
from flask_restful import reqparse,Resource, Api,request,url_for
from pymongo import MongoClient
from pymongo import collection

from jetuser import *

from leancloud import Object,Query
from pymongo import read_preferences
import util
import random
app = Flask(__name__)
api = Api(app)

from celery import Celery
import os 

import requests
capp = Celery('smstasks', broker=os.environ.get('CELERY_BROKER_URL',"amqp://guest@1257.net"))

def quicksend(phone,smscode):
    
        payload = {'method': 'Submit', 'account': 'cf_xingfaner','password':'1234567','mobile':phone,'content':"您的验证码是：%s。请不要把验证码泄露给其他人。"%(smscode)}

        ret =requests.get('http://106.ihuyi.cn/webservice/sms.php',params=payload)
        print 'ret=',ret.text

        
def newSmslog1( phone,smscode):
            client = MongoClient(util.getMydbip())

            db = client.test_database
            ret = db['smslog'].find_one({'phone':phone})
            if ret is None:
                ret = db['smslog'].insert({"phone":phone,"smscode":smscode})
                print 'ret=',ret
            else:
                ret = db['smslog'].update ({'phone':phone}, {"$set": { "smscode":smscode }})
                print 'ret=',ret              
          
            client.close()
def querySmslog1(smscode):
            client = MongoClient(util.getMydbip())

            db = client.test_database
            ret = db['smslog'].find_one({'smscode':smscode})
            print 'ret=',ret
            if ret is not None:
                client.close()
            
                return ret['phone']
            else:
                client.close()
                None

def newSmslogpass( phone,smscode):
            client = MongoClient(util.getMydbip())

            db = client.test_database
            ret = db['smslogpass'].find_one({'phone':phone})
            if ret is None:
                ret = db['smslogpass'].insert({"phone":phone,"smscode":smscode})
                print 'ret=',ret
            else:
                ret = db['smslogpass'].update ({'phone':phone}, {"$set": { "smscode":smscode }})
                print 'ret=',ret              
          
            client.close()
def querySmslogpass(smscode):
            client = MongoClient(util.getMydbip())

            db = client.test_database
            ret = db['smslogpass'].find_one({'smscode':smscode})
            print 'ret=',ret
            if ret is not None:
                client.close()
            
                return ret['phone']
            else:
                client.close()
                None
def newSmslog(phone,smscode):
    smscodelog= Object.extend('smscodelog')
    s = smscodelog()
    s.set("phone",phone)
    s.set("smscode",smscode)
    s.save()

def newSmscode():
    selectedRandomNumber= random.randint(1,999999)
    return str(selectedRandomNumber).zfill(6)
def querySmslog(smscode):
    try:
            mytest = Object.extend("smscodelog")
            query = Query(mytest)
#            query.not_equal_to("status", 4)
#            query.not_equal_to("status", 5)
            query.equal_to("smscode",smscode)         
            olds = query.first

    except Exception,e:
        print 'e=',
    return [] 




@app.route('/1.1/requestPasswordResetBySmsCode', methods=['post'])
def requestPasswordResetBySmsCode():
     try:
            print 'requestPasswordResetBySmsCode'
            print "put request=",request.json
            username = request.json.get('mobilePhoneNumber')
            print 'username=',username
            if username is None :
                abort(400)    # missing arguments
#            User.objects.all()
            print 'username=',username

#            user =User.objects.filter(username=username).first()
#            if  user is not None:
            if  username is not None:
                print 'not None'
                try:

                        print 'build_smscode ok'
#                        send push
                        newsmscode = newSmscode()
                        print 'newsmscode',newsmscode
                        newSmslogpass(username,newsmscode)
#                        capp.send_task('smscloud.smstasks.sendsms', args=[username, newsmscode], kwargs={})
                        quicksend(username, newsmscode)   
                        return (jsonify({'status': "ok"}), 200)

                except Exception,e:
                    print e
                    return (jsonify({'status': "fail"}), 400)
            else:
                return (jsonify({'status': "fail"}), 400)
        #    db.session.add(user)
        #    db.session.commit()

     except Exception,e:
            print e
            
            


@app.route('/1.1/requestMobilePhoneVerify', methods=['post'])
def MobilePhonelogin():
     try:
            print 'MobilePhonelogin'
            print "put request=",request.json
            username = request.json.get('mobilePhoneNumber')
            print 'username=',username
            if username is None :
                abort(400)    # missing arguments
#            User.objects.all()
            print 'username=',username

#            user =User.objects.filter(username=username).first()
#            if  user is not None:
            if  username is not None:
                print 'not None'
                try:

                        print 'build_smscode ok'
#                        send push
                        newsmscode = newSmscode()
                        print 'newsmscode',newsmscode
                        newSmslog1(username,newsmscode)
                        capp.send_task('smscloud.smstasks.sendsms', args=[username, newsmscode], kwargs={})
    
                        return (jsonify({'status': "ok"}), 200)

                except Exception,e:
                    print e
                    return (jsonify({'status': "fail"}), 400)
            else:
                return (jsonify({'status': "fail"}), 400)
        #    db.session.add(user)
        #    db.session.commit()

     except Exception,e:
            print e
            


@app.route('/1.1/requestMobilePhoneVerifyold', methods=['post'])
def MobilePhoneloginold():
     try:
            print 'MobilePhonelogin'
            print "put request=",request.json
            username = request.json.get('mobilePhoneNumber')
            print 'username=',username
            if username is None :
                abort(400)    # missing arguments
            User.objects.all()
            print 'username=',username

            user =User.objects.filter(username=username).first()
            if  user is not None:
                print 'not None'
                try:
                    if user.build_smscode():
                        print 'build_smscode ok'
#                        send push
                        newsmscode = newSmscode()
                        capp.send_task('smscloud.smstasks.sendsms', args=[username, newsmscode], kwargs={})
    
                        return (jsonify({'status': "ok"}), 200)
                    else:
                        return (jsonify({'status': "fail"}), 200)
                except Exception,e:
                    print e
                    return (jsonify({'status': "fail"}), 400)
            else:
                return (jsonify({'status': "fail"}), 400)
        #    db.session.add(user)
        #    db.session.commit()
            return (jsonify({'username': user.username}), 201)
     except Exception,e:
            print e
@app.route('/1.1/verifyMobilePhoneold/<path:smscode>', methods=['post'])
def verifyMobilePhoneold(smscode):
     try:
            print 'login'
#            X-AVOSCloud-Session-Token

            value = request.headers.get('X-AVOSCloud-Session-Token')
            print 'value=',value
            user = User.verify_auth_token(app.config['SECRET_KEY'],value)
            if user  is   None:
                 return (jsonify({'status': "fail"}), 400)
            if  user is not None:
                try:
                    if user.verify_smscode(smscode):
                        print 'verify_smscode ok'
                        oid = str(user.id)
                        return (jsonify({'username': user.username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)
                    else:
                        return (jsonify({'status': "fail"}), 400)
                except Exception,e:
                    print e
                    return (jsonify({'status': "fail"}), 400)
            else:
                return (jsonify({'status': "fail"}), 400)

     except Exception,e:
            print e

@app.route('/1.1/verifyMobilePhone/<path:smscode>', methods=['post'])
def verifyMobilePhone(smscode):
     try:
            print 'verifyMobilePhone',smscode
#            X-AVOSCloud-Session-Token
            ret = querySmslog1(smscode)
            
            if ret is not None:
                return (jsonify({'status': "ok"}), 200)
            else:
                return (jsonify({'status': "fail"}), 400)
                 

     except Exception,e:
            print e    

@app.route('/1.1/resetPasswordBySmsCode/<path:smscode>', methods=['PUT'])
def resetPasswordBySmsCode(smscode):
     try:
            print 'resetPasswordBySmsCode',smscode
            newpassword = request.json.get('password')
            print 'newpassword=',newpassword
            if newpassword is None :
                abort(400)    # missing arguments
                
            
#            X-AVOSCloud-Session-Token
            retphone = querySmslogpass(smscode)
            
            if retphone is not None:
                print 'ret mobilephone',retphone
                olduser = User.objects.filter(username=retphone).first()
                
                if olduser is not None:
                   print 'exist user'
                   olduser.password= newpassword
                   olduser.hash_password(newpassword)
                   olduser.save()
                   return (jsonify({'status': "ok"}), 200)
                        
                return  (jsonify({'status': "fail"}), 400)   # existing user
            else:
                return (jsonify({'status': "fail"}), 400)
                 

     except Exception,e:
            print e 
                            
if __name__ == '__main__':

    connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
                     
    capp.send_task('smscloud.smstasks.sendsms', args=["13906917736", "456789"], kwargs={})
    
    app.run(host="0.0.0.0",debug=True)