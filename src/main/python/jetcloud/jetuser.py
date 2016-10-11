'''
Created on 2015

@author: aadebuger
'''
from mongoengine import * 

import time
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
class User(DynamicDocument):
#    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    username = StringField(required=True)
    createdAt = StringField(required=True)
    updatedAt = StringField(required=True)
 
    
    activated = BooleanField(default=False)
    
    mobilePhoneVerified=BooleanField(default=False)
    emailVerified=BooleanField(default=False)
    smscode = StringField(required=False)
    phone = StringField(required=False)
    email = EmailField()
    MobilePhoneNumber =StringField()
    phonenum=StringField()
    sessionToken=StringField(required=False)
    obarberid =StringField()
    oshopid  = StringField() 
    pushGroupId=ListField()
    commonaddress=ListField()
    pushId=StringField()
    objectId=StringField()
    sex = StringField()
    nickname = StringField()
    imgurl=StringField()
    hairstyle = StringField()
    likehairstyle=StringField()
    
    authData = DictField()
    
    
    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)
        
    def verify_password(self, password):
        print 'self.password_hash',self.password
        return pwd_context.verify(password, self.password)    

    def build_smscode(self):
#        self.generate_auth_token()
        
        self.smscode="123456"
        if len(self.username)>=6:
            self.smscode = self.username[-6:]
#        self.createdAt=time.strftime('%Y-%m-%dT%H:%M:%S')
        self.updatedAt=time.strftime('%Y-%m-%dT%H:%M:%S')
        self.save()    
        return True
         
    def generate_auth_token(self, secret_key,expiration=3600000):
        s = Serializer(secret_key, expires_in=expiration)
        print 'self.id =',self.id
        self.sessionToken=s.dumps(str(self.id))
        print 'self sessionToken=',self.sessionToken
#     return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(secret_key,token):
        
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            print 'none1'
            return None    # valid token, but expired
        except BadSignature:
            print 'none2'
            return None    # invalid token
        print 'data=',data
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
    @staticmethod
    def querybyauthData(service,openid):

        
        key= "authData_%s_%s"%(service,"openid")
        user =User.objects(key=openid).first()       
        
        return user    

if __name__ == '__main__':
    pass