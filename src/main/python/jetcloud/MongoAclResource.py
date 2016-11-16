'''
Created on 2015

@author: aadebuger
'''
import MongoResource

from flask import Flask, request
#from flask.ext.restful import reqparse, abort, Api, Resource
from flask_restful import Resource, Api

from pymongo import MongoClient
from pymongo import collection
from pymongo import collection
from bson import json_util
from bson.objectid import ObjectId

from MongoResource import MResource,MResourceList
from MongoResource import getMclient,getIso8601
import util

import json
#from  jetcloudrest import User
#import jetcloudrest
from jetuser import *
def getObjectid(request,appsecretkey):
            value = request.headers.get('X-AVOSCloud-Session-Token')
            print 'value1=',value
            if value is None:
                return None
            print 'verify'
            user = User.verify_auth_token(appsecretkey,value)

            return user

def getUserAcl(request,appsecretkey):
    aclcondition = {}
    user = getObjectid(request,appsecretkey)
    print 'user=',user
    if user is None:
        return {'userid': "none"}
    aclcondition = {'userid': str(user.id)}
    return aclcondition
                 
def getBarberUserAcl(request,appsecretkey):
    aclcondition = {}
    user = getObjectid(request,appsecretkey)
    print 'user=',user
    if user is None:
        return {'obrberid': {"$in": "none"}}
    aclcondition = {'obarberid':{"$in": str(user.id)}}
    return aclcondition
                 
                            
class MAclResource(MResource):
    '''
    classdocs
    '''


    def __init__(self,documentname,appsecretkey):
        '''
        Constructor
        '''
        self.documentname =documentname
        self.appsecretkey = appsecretkey
    def get(self, todo_id):
        return MResource.get(self,todo_id)
 
    def delete(self, todo_id):
        print 'todo_id',todo_id
        user = getObjectid(request);
        print 'user=',user
        if  user is None:
                return 'fail',400
        
#        abort_if_todo_doesnt_exist(todo_id)
        client = getMclient()
        db = client.test_database
        op = getUserAcl(self.appsecretkey,request)
        print 'op=',op
        mydict={}
        mydict['_id'] =  ObjectId(todo_id)
        for (d,x) in op.items():
                    mydict[d]=x
                    
        try:
                ret  = db[self.documentname].remove(mydict,safe=True)   
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
            op = getUserAcl(self.appsecretkey,request)
            print 'op=',op
            dict={}
            dict['_id'] =  ObjectId(todo_id)
            for (d,x) in op.items():
                    dict[d]=x

            request.json['updatedAt']=MongoResource.getIso8601()
            if opword=='':
                ret = db[self.documentname].update(dict,{"$set":request.json})      
            else:
                ret = db[self.documentname].update(dict,{opword:request.json}) 
            print 'ret=',ret
            retdict = {"id":todo_id,"updatedAt":request.json['updatedAt']}
            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201
    
 
class MAclResourceList(MResourceList):
    def __init__(self,documentname,getacl):
        '''
        Constructor
        '''
        self.documentname =documentname
        self.getacl = getacl
    def before_save(self):
        return True;
    def after_save(self):
        print 'after_save1'
    def get(self):
        print 'acl get'
 #       args = parser.parse_args()
 #       print 'args=',args        
#        client = MongoClient(util.getMydbip())
        client = getMclient()
        db = client.test_database
        print "list get=",request
        searchword = request.args.get('where', '')
#        offset = int(request.args.get('offset', '0'))
        offset = int(request.args.get('skip', '0'))

        limit = int(request.args.get('limit', '0'))
        order= request.args.get('order', '')
        
        
        print 'MAclResourceList self getacl',self.getacl
        op = self.getacl(self.appsecretkey,request)
        print 'op=',op
        print 'searchword=',searchword
        print 'offset=',offset
        print 'limit=',limit
        print 'order=',order
        
        
#        ret = db.news.find_one()
        if searchword=='' or searchword=='{}':
            print 'searchword=null'
#sort({"createdAt":-1})            
            try: 
                    if limit==0:
                        if offset ==0:
                            ret = db[self.documentname].find(op).sort([('_id', -1)])
                        else:
                            ret = db[self.documentname].find(op).sort([('_id', -1)]).offset(offset);
                    else:
                        if offset == 0 :
                            ret = db[self.documentname].find(op).sort([('_id', -1)]).limit(limit)
                        else:
                            ret = db[self.documentname].find(op).sort([('_id', -1)]).skip(offset).limit(limit)
            except Exception,e:
                    print e
        else:
             dict = json.loads(searchword)
             for (d,x) in op.items():
                    dict[d]=x
             if dict.has_key("objectId"):
                    oid = dict["objectId"]
                    dict['_id']=ObjectId(oid)
                    del dict["objectId"]
             if dict.has_key("location"):
                     print 'location=',dict['location']
                     mylocation = dict['location']
                     if mylocation.has_key('$nearSphere'):
                             mylocation['$near'] = mylocation['$nearSphere']
                             del mylocation['$near']["__type"]
#                            mylocation['$near']={'latitude': 39.9087144,  ,'longitude': 116.397389}
                            
                             del mylocation['$nearSphere']
#                    del dict['location']
             print 'new dict=',dict
             ret = db[self.documentname].find(dict)
             orderv = order.split(",")
             print 'orderv=',orderv
             if order is not "":
                 print 'order sort'
                 for sortvalue in orderv:
                
                    if sortvalue.startswith("-"):
                         ret.sort(sortvalue[1],-1)
                    else:
                        ret.sort(sortvalue)
        newsv = [];
        for news in ret:
            if news.get("id")==None:
                oid =  str(news["_id"])
                del news["_id"]
#                news['id']=oid
                news['objectId']=oid
                print 'oid=',oid
            newsv.append(news)
#        print 'newsv=',newsv
        retdict={}
        retdict['results']=newsv
#        return json.dumps(newsv,default=json_util.default)        
        retstr= json.dumps(newsv,default=json_util.default)  
        newdict = json.loads(retstr)  
#        client.close()
        return retdict
    def post(self):
        print "post=",request
        if not self.before_save():
             return "111",404
        
        try:
            print "post request=",request.json
#            client = MongoClient(util.getMydbip())
            client = getMclient()
        
            db = client.test_database

            timestr =getIso8601()
            request.json['createdAt']=timestr
            request.json['updatedAt']=timestr
            op = getUserAcl(self.appsecretkey,request)
            print 'op=',op
            for (d,x) in op.items():
                    request.json[d]=x
                     
            if request.json.has_key("location"):
                    print 'find location'
                    location = request.json['location']
                    del location["__type"]
                    
            ret = db[self.documentname].insert(request.json)      
            print str(ret)
            retdict = {"objectId":str(ret),'createdAt':timestr}
            self.after_save();
#            return json.dumps(retdict),201
 #           client.close()
            return retdict
           
        except Exception,e:
            print e
        return "111"   
    
if __name__ == '__main__':
    pass