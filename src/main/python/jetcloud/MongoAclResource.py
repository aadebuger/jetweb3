'''
Created on 2015

@author: aadebuger
'''
import MongoResource

from flask import Flask, request
from flask.ext.restful import reqparse, abort, Api, Resource
from pymongo import MongoClient
from pymongo import collection
from pymongo import collection
from bson import json_util
from bson.objectid import ObjectId

from MongoResource import MResource

import util
#from  jetcloudrest import User
#import jetcloudrest
def getObjectid(request):
            value = request.headers.get('X-AVOSCloud-Session-Token')
            print 'value=',value
            if value is None:
                return None
            user = jetcloudrest.User.verify_auth_token(value)
            return user
            
class MAclResource(MResource):
    '''
    classdocs
    '''


    def __init__(self,documentname):
        '''
        Constructor
        '''
        self.documentname =documentname
    def get(self, todo_id):
        return MResource.get(self,todo_id)
 
    def delete(self, todo_id):
        print 'todo_id',todo_id
        user = getObjectid(request);
        print 'user=',user
        if  user is None:
                return 'fail',400
        
#        abort_if_todo_doesnt_exist(todo_id)
        client = MongoClient(util.getMydbip())
        db = client.test_database
        try:
                ret  = db[self.documentname].remove({'_id': ObjectId(todo_id),'ownid':user.id},safe=True)   
                print 'ret=',ret     
                return '', 204
        except Exception, e:
            print e
    def put(self, todo_id):
        print "put=",request
        print 'todo_id',todo_id
        try:
            print "put request=",request.json
#            newtodo_id = request.json['id'];
#            print "newtodo_id=",newtodo_id;
            client = MongoClient(util.getMydbip())
            try:
                del request.json["id"];
            except Exception,e:
                    print e
            db = client.test_database
            opword = request.args.get('op', '')
            print 'opword=',opword;
            updatedAt= time.strftime('%Y-%m-%d %H:%M:%S')
            request.json['updatedAt']=time.strftime('%Y-%m-%d %H:%M:%S')
            if opword=='':
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{"$set":request.json})      
            else:
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{opword:request.json}) 
            print 'ret=',ret
            retdict = {"id":todo_id,"updatedAt":updatedAt}
            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201
    
    
    
if __name__ == '__main__':
    pass