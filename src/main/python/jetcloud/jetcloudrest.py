# -*- coding: utf-8 -*-
'''
Created on 2015年5月29日

@author: aadebuger
'''
from flask import Flask
from flask import abort,jsonify
from flask_restful import reqparse,Resource, Api,request,url_for

import sys
import json
import cloudfile
from mongoengine import * 
from pymongo import read_preferences
import util
from passlib.apps import custom_app_context as pwd_context
from functools import wraps
from flask import make_response
import time

from pymongo import MongoClient
import MongoResource
import MongoAclResource
from bson import ObjectId
import base64
import cStringIO
from bson import json_util
#import jetuser
from jetuser import *
#from jetcloud.MongoAclResource import getUserAcl
app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'i love beijing tianmen yeah'

parser = reqparse.RequestParser()
parser.add_argument('title', type=str)

def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
         rst = make_response(fun(*args, **kwargs))
         rst.headers['Access-Control-Allow-Origin'] = '*'
         rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
         allow_headers ="Referer,Accept,Origin,User-Agent"
         rst.headers['Access-Control-Allow-Headers'] = allow_headers
         return rst
    return wrapper_fun

  


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
@app.route('/1.1/filesdirect/<path:filename>', methods=['POST'])
def save_upload(filename):

#    file = request.files['file']
#    print 'file=',file

#    if file and allowed_file(file.filename):
#        print 'data len',len(request.data)
        
        mediaid = MongoResource.newUpload("media");                
#        filename = secure_filename(file.filename)
        print 'filename=',filename
#        mongo.save_file("%s.jpg"%(mediaid), request.files['file'])
  
        cloudfile.uploadfile(filename,request.data)
        url="http://7xjdvj.com1.z0.glb.clouddn.com/%s"%(filename)
        name=filename
        retdict= MongoResource.newBucketUpload("files", len(request.data), "jetcloud",url, name)

        print 'retdict=',retdict    
        return json.dumps(retdict);
        
#        abort(404, message="mimetype error")


@app.route('/1.1/files/<path:filename>', methods=['POST'])
def save_uploadform(filename):

#    file = request.files['file']
#    print 'file=',file

#    if file and allowed_file(file.filename):
#        print 'data len',len(request.data)
        
#        mediaid = MongoResource.newUpload("media");                
#        filename = secure_filename(file.filename)
        print 'filename=',filename
#        mongo.save_file("%s.jpg"%(mediaid), request.files['file'])
        
        form = request.get_json() 
        print 'form=',form
        print '_ContentType',form['_ContentType']
        print 'mime_type',form['mime_type']
        print 'metaData',form['metaData']
        
#        abort(404, message="mimetype error") 
        pic = cStringIO.StringIO()
        image_string = cStringIO.StringIO(base64.b64decode(form['base64']))
        cloudfile.uploadfile(filename,image_string )
        url="http://7xjdvj.com1.z0.glb.clouddn.com/%s"%(filename)
        name=filename
        retdict= MongoResource.newBucketUpload("files", len(request.data), "jetcloud",url, name)

        print 'retdict=',retdict    
        return json.dumps(retdict);
        
#        abort(404, message="mimetype error")
@app.route('/1.1/neworderno', methods=['get'])
def newOrderno():
            neworderno = MongoResource.newOrderno("number")
            return (jsonify({'orderno': neworderno}), 200)

@app.route('/1.1/classes/_User/<path:oid>', methods=['get'])
def get_user(oid):
     try:
            print 'get_user'


            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'get user next'
            print 'user.id=',user.id
            oid = str(user.id)
            return (jsonify({'sessionToken':user.sessionToken,'username': user.username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})


#  the import things safe 
@app.route('/1.1/users/<path:oid>', methods=['delete'])
def removemobileuseronlytest(oid):
     try:
            print 'get_user'
            _SessionToken= request.headers.get('X-AVOSCloud-Session-Token')

            
            print '_SessionToken=',_SessionToken
#            user = User.verify_auth_token(app.config['SECRET_KEY'],_SessionToken)
#            print 'session user=',user

            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'user=',user
            user.delete();
            return jsonify({"code":200})
     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})



@app.route('/1.1/users/<path:oid>', methods=['get'])
def getmobileuser(oid):
     try:
            print 'get_user'
            _SessionToken= request.headers.get('X-AVOSCloud-Session-Token')

            
            print '_SessionToken=',_SessionToken
#            user = User.verify_auth_token(app.config['SECRET_KEY'],_SessionToken)
#            print 'session user=',user

            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'get user next'
            print 'user.id=',user.id
            oid = str(user.id)
            userjson = json_util.dumps(user)
            print 'userjson',userjson
            newuserjson = MongoResource.getDocument('user',user.id)
            print 'newuserjson',newuserjson
            return newuserjson
#            return (jsonify({'sessionToken':user.sessionToken,'username': user.username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})





@app.route('/1.1/classes/_User', methods=['get'])
def get_userbywhere():
     try:
            print 'get_user'

            searchword = request.args.get('where', '')
            print 'searchword=',searchword

            client = MongoClient(util.getMydbip())
            db = client.stylemaster
            if searchword =='':

                ret = db["user"].find()
            else:
                dict = json.loads(searchword)
                if dict.has_key("objectId"):
                    dict['_id']=ObjectId(dict['objectId'])
                    del dict['objectId']
                print 'dict=',dict
                ret = db["user"].find(dict)
            newsv = [];
            print 'ret=',ret
            for news in ret:
                print 'news=',news
                print 'news get id',news.get("id")
                if news.get("id")==None:
                    oid =  str(news["_id"])
                    del news["_id"]
#                    news['id']=oid
                    news['objectId']=oid                    
                newsv.append(news)
            print 'newsv=',newsv
            retdict={}
            retdict['results']=newsv
            client.close()
            return jsonify(retdict)
#            return jsonify({'sessionToken':user.sessionToken,'username': user.username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} )

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})
     return  (jsonify({'status': "fail"}), 400)       

@app.route('/1.1/classes/_User/<path:oid>', methods=['put'])
def put_user(oid):
     try:
            print 'get_user'

            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'get user next'
            print 'user.id=',user.id
            print "put request=",request.json
            dict = request.json
            if dict.has_key("password"):
                password = request.json["password"]
                request.json["password"] =pwd_context.encrypt(password)
                
            request.json['updatedAt']=MongoResource.getIso8601()
            
            MongoResource.updateDocument("user",user.id,request.json)
            oid = str(user.id)
            return (jsonify({"updatedAt":user.updatedAt,"objectId":oid} ), 200)

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/1.1/users/<path:oid>', methods=['put'])
def putmobileuser(oid):
     try:
            print 'get_user'
            paramdict = json.loads(request.data)
            print 'paramdict=',paramdict

            _SessionToken= request.headers.get('X-AVOSCloud-Session-Token')

            
            print '_SessionTokenput=',_SessionToken
            user = User.verify_auth_token(app.config['SECRET_KEY'],_SessionToken)
            print 'session userput=',user
            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'get user nextput'
            print 'putuser.id=',user.id

            if isinstance(paramdict, dict):
                        print 'dict'
            if paramdict.has_key("password"):
                 print 'remove password'
                 del paramdict['password']
            print 'test11'
#                password = request.json["password"]
#                request.json["password"] =pwd_context.encrypt(password)
                

#            if paramdict.has_key['objectId']:
#                    print 'remove objectId'
#                    del paramdict['objectId']
            if paramdict.has_key("objectId"):
                 print 'remove password'
                 del paramdict['objectId']
            print 'test12'
            if paramdict.has_key('sessionToken'):
                    del paramdict['sessionToken']
            print 'test2'
            paramdict['updatedAt']=MongoResource.getIso8601()
            MongoResource.updateDocument("user",user.id,paramdict)
            oid = str(user.id)
            return (jsonify({"updatedAt":user.updatedAt,"objectId":oid} ), 200)

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/1.1/classes/_User', methods=['POST'])
def new_user():
     try:
            print 'new_user'
            username = request.json.get('username')
            password = request.json.get('password')
            if username is None or password is None:
#               abort(400)    # missing arguments
                return (jsonify({'status': "fail"}), 400)
            print 'username=',username
            print 'password=',password
            User.objects.all()
            print 'test1'
            if User.objects.filter(username=username).first() is not None:
                   print 'exist user'
                   return  (jsonify({'status': "fail"}), 400)   # existing user

            print 'new user next'
            user = User(username=username)
            user.hash_password(password)
            user.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            user.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            user.generate_auth_token(app.config['SECRET_KEY'])
            obarberid = request.json.get('obarberid')
            oshopid = request.json.get("oshopid")
            if obarberid is not None:
                    print 'obarberid  not none'
                    user.obarberid=obarberid
            if oshopid is not None:
                    print 'oshopid not none'
                    user.oshopid=oshopid
            
                        
            print 'sessionToken',user.sessionToken
            user.save()
        #    db.session.add(user)
        #    db.session.commit()
            print 'user.id=',user.id
            oid = str(user.id)
            return jsonify({ "objectId":oid,'sessionToken':user.sessionToken,"createdAt":user.createdAt,"updatedAt":user.updatedAt})
        
#            return (jsonify({ 'sessionToken':user.sessionToken,"createdAt":user.createdAt,"updatedAt":user.updatedAt}), 201,{'Location': url_for('/1.1/users', id=oid)})
     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})


@app.route('/1.1/users', methods=['POST'])
def newmobileuser():
     try:
            print 'new_user'
            print 'json=',request.json
            username = request.json.get('username')
            password = request.json.get('password')
            if username is None or password is None:
#               abort(400)    # missing arguments
                return (jsonify({'status': "fail"}), 400)
            print 'username=',username
            print 'password=',password
            User.objects.all()
            print 'test1'
            if User.objects.filter(username=username).first() is not None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'new user next'
            user = User(username=username)
            user.hash_password(password)
#            user.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
#            user.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            user.createdAt=MongoResource.getIso8601()
            user.updatedAt=MongoResource.getIso8601()   
            if  request.json.has_key("oshopid"):
                print 'oshop exists'
                user.oshopid= request.json.get('oshopid')      
            user.save()
        #    db.session.add(user)
        #    db.session.commit()
            print 'user.id=',user.id
            user.generate_auth_token(app.config['SECRET_KEY'])
            print 'sessionToken',user.sessionToken
            user.save()
            oid = str(user.id)
            return jsonify({ "objectId":oid,'sessionToken':user.sessionToken,"createdAt":user.createdAt,"updatedAt":user.updatedAt})
        
#            return (jsonify({ 'sessionToken':user.sessionToken,"createdAt":user.createdAt,"updatedAt":user.updatedAt}), 201,{'Location': url_for('/1.1/users', id=oid)})
     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/1.1/login', methods=['get'])
def login():
     try:
            print 'login'
            username = request.args.get('username')
            password = request.args.get('password')
            if username is None or password is None:
                abort(400)    # missing arguments
            print 'username=',username
            print 'password=',password
            user =User.objects.filter(username=username).first()
            if  user is not None:
                try:
                    if user.verify_password(password):
                        print 'verify_password ok'
                        user.generate_auth_token(app.config['SECRET_KEY'])
                        print 'new sessiontoken', user.sessionToken        
                        oid = str(user.id)
                        if user.obarberid is not None:
                            return (jsonify({'obarberid':user.obarberid,'sessionToken':user.sessionToken,'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)                        
                        else:           
                            return (jsonify({'sessionToken':user.sessionToken,'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)
                    else:
                       return (jsonify({"code":210,"error":"The username and password mismatch."}), 400)
                except Exception,e:
                    print e
                    return (jsonify({'status': "fail"}), 400)
            else:
                print 'user is None'
                return (jsonify({'status': "fail"}), 400)
        #    db.session.add(user)
        #    db.session.commit()
            return (jsonify({'username': user.username}), 201)
     except Exception,e:
            print e
@app.route('/1.1/login', methods=['post'])
def loginbypost():
     try:
            print 'login post'
            print 'json=',request.json
            paramdict = request.json
            if paramdict is None:
                        paramdict = json.loads(request.data)
                        
            username = paramdict.get('username')
            password = paramdict.get('password')
            if username is None or password is None:
                abort(400)    # missing arguments
            print 'username=',username
            print 'password=',password
            user =User.objects.filter(username=username).first()
            if  user is not None:
                try:
                    if user.verify_password(password):
                        print 'verify_password ok'
                        user.generate_auth_token(app.config['SECRET_KEY'])
                        print 'new sessiontoken', user.sessionToken 
                        oid = str(user.id)
                        if user.obarberid is not None:
                            return (jsonify({'obarberid':user.obarberid,'sessionToken':user.sessionToken,'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)                        
                        else: 
                            return (jsonify({'sessionToken':user.sessionToken,'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)
                    else:
                        return (jsonify({"code":210,"error":"The username and password mismatch."}), 200)
                except Exception,e:
                    print e
                    return (jsonify({"code":210,"error":"The username and password mismatch."}), 400)
            else:
                return (jsonify({"code":210,"error":"The username and password mismatch."}), 400)
        #    db.session.add(user)
        #    db.session.commit()
            return (jsonify({'username': user.username}), 201)
     except Exception,e:
            print e

@app.route('/1.1/requestMobilePhoneVerify', methods=['post'])
def MobilePhonelogin():
     try:
            print 'login'
            username = request.args.get('mobilePhoneNumber')
            if username is None :
                abort(400)    # missing arguments
            print 'username=',username

            user =User.objects.filter(username=username).first()
            if  user is not None:
                try:
                    if user.build_smscode():
                        print 'build_smscode ok'
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
@app.route('/1.1/requestLoginSmsCode', methods=['post'])
def requestLoginSmsCode():
     try:
            print 'login'
            username = request.args.get('mobilePhoneNumber')
            if username is None :
                abort(400)    # missing arguments
            print 'username=',username

            user =User.objects.filter(username=username).first()
            if  user is not None:
                try:
                    if user.build_smscode():
                        print 'build_smscode ok'
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
            
@app.route('/1.1/usersByMobilePhone', methods=['post'])
def usersByMobilePhone():
     try:
            print 'login'
            username = request.args.get('mobilePhoneNumber')
            password = request.args.get('smsCode')
            if username is None or password is None:
                abort(400)    # missing arguments
            print 'username=',username
            print 'password=',password
            user =User.objects.filter(username=username).first()
            if  user is not None:
                try:
                    if user.verify_smscode(password):
                        print 'verify_smscode ok'
                        oid = str(user.id)
                        return (jsonify({'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)
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
@app.route('/1.1/verifyMobilePhone/<path:smscode>', methods=['post'])
def verifyMobilePhone(smscode):
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
 

@app.route('/1.1/users/<string:todo_id>/updatePassword', methods=['put'])
def updatePassword(todo_id):
     try:
            print 'todo_id1',todo_id
            paramdict = json.loads(request.data)
            print 'paramdict=',paramdict

            old_password = paramdict.get('old_password')
            new_password= paramdict.get("new_password")
            print 'new_password',new_password


            _SessionToken = request.headers.get('X-AVOSCloud-Session-Token')
            print '_SessionToken value=',value

            print '_SessionToken=',_SessionToken
            user = User.verify_auth_token(app.config['SECRET_KEY'],_SessionToken)
            print 'session user=',user
#           user= User.objects(pk=todo_id).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            if user.verify_password(old_password):
                         print 'verify_password ok'  
                         user.hash_password(new_password)
                         user.updatedAt=MongoResource.getIso8601() 
                         user.save()
                         return (jsonify({"updatedAt":user.updatedAt,"objectId":todo_id} ), 200)

                        
            return (jsonify({"code":210,"error":"The username and password mismatch."}), 400)
            return 
     except Exception,e:
            print e  



            
             
   
@app.route('/1.1/batch/save', methods=['post'])
def batch():
         print 'batch request json',request.json
         return (jsonify({'status': "fail"}), 400)

@app.route('/1.1/cloudQuery', methods=['get'])
def cloudQuery():

            print 'cloudQuery'
            cql = request.args.get('cql')
            
            print 'cql=',cql
            documentname="barber"
            queryvalue="hello"
            MongoResource.searchDocument(document,{},queryvalue,0,10,"")
            retdict={}
            retdict['results']=[]
            retstr= json.dumps(retdict,default=json_util.default) 
            return retstr        

class Barber(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="barber"
class BarberList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="barber"


class Shop(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="shop"
class ShopList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="shop"

class Hairstyle(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="hairstyle"
class HairstyleList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="hairstyle"    

class Order(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"
        self.projectfields ={"charge":0,"latitude":0}
class OrderList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"     
#        self.projectfields ={"charge":0,"latitude":0}
        self.projectfields ={"charge":0,"latitude":0,"longitude":0}
    def after_save(self,objectid,action):
        
        print 'after_save order',objectid,action  
        MongoResource.pushEvent("order",objectid,{}, "post")    


class YhOrder(MongoAclResource.MAclResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"
        self.projectfields ={"charge":0,"latitude":0}
        self.getacl = MongoAclResource.getUserAcl
class YhOrderList(MongoAclResource.MAclResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"   
        self.appsecretkey =app.config['SECRET_KEY']
#        self.projectfields ={"charge":0,"latitude":0}
        self.projectfields ={"charge":0,"latitude":0,"longitude":0}
        self.getacl = MongoAclResource.getUserAcl
        print 'self getacl',self.getacl                
    def after_save(self,objectid,action):
        
        print 'after_save order',objectid,action  
        MongoResource.pushEvent("order",objectid,{}, "post") 
        

class BarberOrder(MongoAclResource.MAclResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"
        self.projectfields ={"charge":0,"latitude":0}
        self.getacl = MongoAclResource.getBarberUserAcl
class BarberOrderList(MongoAclResource.MAclResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="order"   
        self.appsecretkey =app.config['SECRET_KEY']
#        self.projectfields ={"charge":0,"latitude":0}
        self.projectfields ={"charge":0,"latitude":0,"longitude":0}
        self.getacl = MongoAclResource.getBarberUserAcl
        print 'self getacl',self.getacl                
    def after_save(self,objectid,action):
        
        print 'after_save order',objectid,action  
        MongoResource.pushEvent("order",objectid,{}, "post")      
        
class Service(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="service"
class ServiceList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="service"   

class Review(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="review"
class ReviewList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="review" 

class Coupon(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="coupon"
class CouponList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="coupon" 
                
                
                                
        
class Makeup(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="makeup"
class MakeupList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="makeup"                     
class Makeupartist(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="makeupartist"
class MakeupartistList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="makeupartist"                     


class Suitpromotion(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="suitpromotion"
class SuitpromotionList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="suitpromotion" 
        
class Appointment(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="appointment"
class AppointmentList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="appointment" 


class Mycollection(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="collection"
    def after_put(self,objectid,datajson,action):
        
        print 'after_putq collection',objectid,action  
        MongoResource.pushEvent("collection",objectid,datajson, "put")   
class MycollectionList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="collection" 
    def after_save(self,objectid,action):
        
        print 'after_save collection',objectid,action  
        MongoResource.pushEvent("collection",objectid,{}, "post")     
  
                
class Role(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="role"
class RoleList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="role" 
        
                                         
                    
class Store(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="story"
class StoreList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="story"
class GameScore(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="GameScore"
class GameScoreList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="GameScore"
class feedback(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="feedback"
class feedbackList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="feedback"


class Event(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="event"
class EventList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="event"
        

class users(MongoAclResource.MAclResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="Users"
# for simple demo test
#ObjectDemoTableRead
class ObjectDemoTableRead(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="ObjectDemoTableRead"
class ObjectDemoTableReadList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="ObjectDemoTableRead"     


api.add_resource(BarberList, '/1.1/classes/barber')
api.add_resource(Barber, '/1.1/classes/barber/<string:todo_id>')



api.add_resource(ShopList, '/1.1/classes/shop')
api.add_resource(Shop, '/1.1/classes/shop/<string:todo_id>')

api.add_resource(HairstyleList, '/1.1/classes/hairstyle')
api.add_resource(Hairstyle, '/1.1/classes/hairstyle/<string:todo_id>')


api.add_resource(ServiceList, '/1.1/classes/service')
api.add_resource(Service, '/1.1/classes/service/<string:todo_id>')


api.add_resource(AppointmentList, '/1.1/classes/appointment')
api.add_resource(Appointment, '/1.1/classes/appointment/<string:todo_id>')


api.add_resource(MycollectionList, '/1.1/classes/collection')
api.add_resource(Mycollection, '/1.1/classes/collection/<string:todo_id>')



api.add_resource(RoleList, '/1.1/classes/role')
api.add_resource(Role, '/1.1/classes/role/<string:todo_id>')


api.add_resource(MakeupList, '/1.1/classes/makeup')
api.add_resource(Makeup, '/1.1/classes/makeup/<string:todo_id>')

api.add_resource(MakeupartistList, '/1.1/classes/makeupartist')
api.add_resource(Makeupartist, '/1.1/classes/makeupartist/<string:todo_id>')

api.add_resource(SuitpromotionList, '/1.1/classes/suitpromotion')
api.add_resource(Suitpromotion, '/1.1/classes/suitpromotion/<string:todo_id>')


api.add_resource(ReviewList, '/1.1/classes/review')
api.add_resource(Review, '/1.1/classes/review/<string:todo_id>')


api.add_resource(CouponList, '/1.1/classes/coupon')
api.add_resource(Coupon, '/1.1/classes/coupon/<string:todo_id>')

api.add_resource(EventList, '/1.1/classes/event')
api.add_resource(Event, '/1.1/classes/event/<string:todo_id>')




api.add_resource(StoreList, '/store')
api.add_resource(Store, '/store/<string:story_id>')
api.add_resource(GameScoreList, '/1.1/classes/GameScore')
api.add_resource(GameScore, '/1.1/classes/GameScore/<string:todo_id>')
api.add_resource(feedbackList, '/1.1/classes/feedback')
api.add_resource(feedback, '/1.1/classes/feedback/<string:todo_id>')


api.add_resource(ObjectDemoTableReadList, '/1.1/classes/ObjectDemoTableRead')
api.add_resource(ObjectDemoTableRead, '/1.1/classes/ObjectDemoTableRead/<string:todo_id>')


api.add_resource(users, '/1.1/classes/users/<string:todo_id>')

def coreRoute():
    api.add_resource(OrderList, '/1.1/classes/order')
    api.add_resource(Order, '/1.1/classes/order/<string:todo_id>')
#  mobile order post
#  mobile order get

def yhRoute():

    api.add_resource(YhOrderList, '/1.1/classes/order')
    api.add_resource(YhOrder, '/1.1/classes/order/<string:todo_id>')
            
#  mobile order  put 

def masterRoute():
    api.add_resource(BarberOrderList, '/1.1/classes/order')
    api.add_resource(BarberOrder, '/1.1/classes/order/<string:todo_id>')    


if __name__ == '__main__':
#    connect('stylemaster',host=util.getMydbip())
    connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)

    if len(sys.argv)>1:
            print 'sys',sys.argv[1]
    else:
        coreRoute()
                    
                    
    app.run(host="0.0.0.0",debug=True)