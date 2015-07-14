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



capp = Celery('smstasks', broker=os.environ.get('CELERY_BROKER_URL',"amqp://guest@1257.net"))

def newSmslog1( phone,smscode):
            client = MongoClient(util.getMydbip())

            db = client.stylemaster
            ret = db[document].insert({"phone":phone,"smscode":smscode})
            print 'ret=',ret
            ret = db["smslog"].insert(dict)  
          
            client.close()
def querySmslog1(smscode):
        pass
    

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

@app.route('/1.1/verifyMobilePhoneold/<path:smscode>', methods=['post'])
def verifyMobilePhone(smscode):
     try:
            print 'verifyMobilePhone',smscode
#            X-AVOSCloud-Session-Token

            return (jsonify({'status': "ok"}), 200)
                    

     except Exception,e:
            print e    
                
if __name__ == '__main__':

    connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
                     
    capp.send_task('smscloud.smstasks.sendsms', args=["13906917736", "456789"], kwargs={})
    
    app.run(host="0.0.0.0",debug=True)