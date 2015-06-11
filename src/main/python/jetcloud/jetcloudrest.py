# -*- coding: utf-8 -*-
'''
Created on 2015年5月29日

@author: aadebuger
'''
from flask import Flask
from flask import abort,jsonify
from flask_restful import Resource, Api,request,url_for
import MongoResource
import json
import cloudfile
from mongoengine import * 
from pymongo import read_preferences
import util
from passlib.apps import custom_app_context as pwd_context
from functools import wraps
from flask import make_response
import time
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'i love beijing tianmen yeah'

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

  

class User(Document):
#    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    username = StringField(required=True)
    createdAt = StringField(required=True)
    updatedAt = StringField(required=True)
 
    
    activated = BooleanField(default=False)
    
    mobilePhoneVerified=BooleanField(default=False)
    emailVerified=BooleanField(default=False)
    smscode = StringField(required=False)
    email = EmailField()
    MobilePhoneNumber =StringField()
    sessionToken=StringField(required=True)
    
    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        print 'self.password_hash',self.password
        return pwd_context.verify(password, self.password)    

    def build_smscode(self):
        self.generate_auth_token()
        
        self.smscode="123456"
        if len(self.username)>=6:
            self.smscode = self.username[-6:]
#        self.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
        self.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
        self.save()    
        
         
    def generate_auth_token(self, expiration=360000):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        self.sessionToken=s.dumps(str(self.id))
        print 'self sessionToken=',self.sessionToken
#     return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            print 'none1'
            return None    # valid token, but expired
        except BadSignature:
            print 'none2'
            return None    # invalid token
        user =User.objects(pk=data).first()
        return user
    @classmethod
    def register(cls, email, password, activated=False, name=''):
        user = cls()
        user.email = email
        user.name = name
        user.activated = activated
        user.set_password(password)
        user.save()

        return user
    
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
@app.route('/1.1/files/<path:filename>', methods=['POST'])
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


@app.route('/1.1/neworderno', methods=['get'])
def newOrderno():
            neworderno = MongoResource.newOrderno("number")
            return (jsonify({'orderno': neworderno}), 200)

@app.route('/1.1/users/<path:oid>', methods=['get'])
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


@app.route('/1.1/users/<path:oid>', methods=['put'])
def put_user(oid):
     try:
            print 'get_user'

            user= User.objects(pk=oid).first()
            if user is None:
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'get user next'
            print 'user.id=',user.id
            print "put request=",request.json
            request.json['updatedAt']=time.strftime('%Y-%m-%d %H:%M:%S')
            updateDocument()
            oid = str(user.id)
            return (jsonify({"updatedAt":user.updatedAt,"objectId":oid} ), 200)

     except Exception,e:
            print e
#    return (jsonify({'username': user.username}), 201,
#            {'Location': url_for('get_user', id=user.id, _external=True)})

@app.route('/api/users', methods=['POST'])
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
               return  (jsonify({'status': "fail"}), 400)   # existing user
            print 'new user next'
            user = User(username=username)
            user.hash_password(password)
            user.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            user.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
            user.generate_auth_token()
            print 'sessionToken',user.sessionToken
            user.save()
        #    db.session.add(user)
        #    db.session.commit()
            print 'user.id=',user.id
            oid = str(user.id)
            return (jsonify({ 'sessionToken':user.sessionToken,"createdAt":user.createdAt,"updatedAt":user.updatedAt}), 201,{'Location': url_for('/1.1/users', id=oid)})
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
                        oid = str(user.id)
                        return (jsonify({'sessionToken':user.sessionToken,'username': username,"createdAt":user.createdAt,"updatedAt":user.updatedAt,"objectId":oid,"mobilePhone":user.MobilePhoneNumber} ), 200)
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
            user = User.verify_auth_token(value)
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
api.add_resource(StoreList, '/store')
api.add_resource(Store, '/store/<string:story_id>')
api.add_resource(GameScoreList, '/1.1/classes/GameScore')
api.add_resource(GameScore, '/1.1/classes/GameScore/<string:todo_id>')
api.add_resource(feedbackList, '/1.1/classes/feedback')
api.add_resource(feedback, '/1.1/classes/feedback/<string:todo_id>')


if __name__ == '__main__':
#    connect('stylemaster',host=util.getMydbip())
    connect('stylemaster',host=util.getMydbip(),read_preference=read_preferences.ReadPreference.PRIMARY)
            
    app.run(host="0.0.0.0",debug=True)