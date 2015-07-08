# -*- coding: utf-8 -*-
'''
Created on 2015年5月30日

@author: aadebuger
'''

import json
from flask import Flask, request
#from flask.ext.restful import reqparse, abort, Api, Resource
from flask_restful import Resource, Api,abort
from pymongo import MongoClient
from pymongo import collection
#from pymongo import ReturnDocument


from pymongo import collection

from bson import json_util
from bson.objectid import ObjectId
import util
import time
from datetime import datetime
import MongodbOperation
from mongoengine import Document, EmailField, StringField, BooleanField, queryset_manager
from passlib.apps import custom_app_context as pwd_context
#from passlib.hash import pbkdf2_sha256
#from passlib.utils import consteq
from pymongo import read_preferences

client1 = MongoClient(util.getMydbip())      
                     
def getMclient():
         return client1

def getIso8601():
   return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]+"Z"
def pushEvent(document,objectjson,datajson,action):
          client = MongoClient(util.getMydbip())

          db = client.test_database
          dict={};
          dict['objectname']=document
          dict['object']= objectjson
          dict['data']= datajson
          
          dict['action']=action
          dict['createdAt']=getIso8601()
          ret = db["event"].insert(dict)  
          print 'push event=',ret
    
    
    
def updateDocument(document,todo_id,json):

            client = MongoClient(util.getMydbip())

            db = client.stylemaster
            ret = db[document].update({'_id': ObjectId(todo_id)},{"$set":json})
            print 'ret=',ret
            client.close()

def getDocument(documentname,todo_id):

            client = MongoClient(util.getMydbip())

            db = client.stylemaster
            document = db[documentname].find_one({'_id': ObjectId(todo_id)})
            print 'document=',document
            if document==None:
                 return""    
#        return json.dumps(document,default=json_util.default)  
            oid =  str(document["_id"])
            del document["_id"]
            del document["password"]
            document['id']=oid
            document['objectId']=oid
            
            retstr = json.dumps(document,default=json_util.default)      
            print 'retstr=',retstr 
            client.close()
            return retstr     


def searchDocument(documentname,projectfields,query,offset, limit,order):
        print 'search'
        
        client = MongoClient(util.getMydbip())
        db = client.test_database

        
        
        
        print 'offset=',offset
        print 'limit=',limit
        print 'order=',order
        
        dict = {'tags':{'$in':query}}
           
#        ret = db.news.find_one()

#        text_results = db.command('text', documentname, search=query, filter={'related':True}, limit=10)

        ret = db[documentname].find(dict,projection=projectfields,skip=offset,limit=limit)
 
 
        newsv=[]
        for news in ret:
            print 'news=',news
            print 'news get id',news.get("id")
            if news.get("id")==None:
                oid =  str(news["_id"])
                del news["_id"]
#                news['id']=oid
                news['objectId']=oid
            newsv.append(news)
        print 'newsv=',newsv
        retdict={}
        retdict['results']=newsv
#        return json.dumps(newsv,default=json_util.default)        
        retstr= json.dumps(newsv,default=json_util.default)  
        newdict = json.loads(retstr)  
        return retdict
    
    
                        
def getNextSequence(documentname):
        print 'getNextSequence'
        client = MongoClient(util.getMydbip())
        db = client.test_database    
#        ret = db[documentname].find_one_and_update(   {'_id': 'userid'}, {'$inc': {'seq': 1}},  projection={'seq': True, '_id': False}, upsert=True, return_document=ReturnDocument.AFTER)
        ret = db[documentname].find_and_modify(   {'_id': 'orderid1'}, {'$inc': {'seq': 1}},  projection={'seq': True, '_id': False}, upsert=True,new=True)

        print ret
        return  ret['seq'];
def newOrderno(document):
            updatedAt= time.strftime('%Y%m%d%H%M%S')
            incnumber = getNextSequence("incnumber")
            order_no = "%s%03d"%(updatedAt,int(incnumber)%1000)
            return order_no
def newUpload(documentname):
        try:
            client = MongoClient(util.getMydbip())
            db = client.test_database
            ret = db[documentname].insert({})      
            print str(ret)
            return str(ret)
        except Exception,e:
            print e
        return None      
def newBucketUpload(documentname,size,bucket,url,name):
        try:
            client = MongoClient(util.getMydbip())
            db = client.test_database
            print 'datetime=',datetime.utcnow()
            print 'datetime=',time.strftime('%Y-%m-%dT%H:%M:%S')
            
            datadict = {"size":size,"bucket":bucket,"url":url,"name":name, "createdAt": time.strftime('%Y-%m-%dT%H:%M:%S')}
            ret = db[documentname].insert(datadict)      
            print str(ret)
            del datadict["_id"]
            datadict['objectId']= str(ret)
            return datadict      
        except Exception,e:
            print e
        return None  
class MResourceList(Resource):
    projectfields={"mtest":0}
    def __init__(self,documentname):
        '''
        Constructor
        '''
        self.documentname =documentname

      
    def before_save(self):
        return True;
    def after_save(self,objectid,action):
        print 'after_save1',objectid,action
    def get1(self):
        print 'get'
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
        
        
        
        print 'searchword=',searchword
        print 'offset=',offset
        print 'limit=',limit
        print 'order=',order
        
        print 'self.projectfields=',self.projectfields
        
#        ret = db.news.find_one()
        if searchword=='' or searchword=='{}':
            print 'searchword=null'
#sort({"createdAt":-1})            
            try: 
                    if limit==0:
                        if offset ==0:
                            ret = db[self.documentname].find({},self.projectfields).sort([('_id', -1)])
                        else:
                            ret = db[self.documentname].find().sort([('_id', -1)]).offset(offset);
                    else:
                        if offset == 0 :
                            ret = db[self.documentname].find().sort([('_id', -1)]).limit(limit)
                        else:
                            ret = db[self.documentname].find().sort([('_id', -1)]).skip(offset).limit(limit)

            except Exception,e:
                    print e
        else:
             dict = json.loads(searchword)
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
             ret = db[self.documentname].find(dict,self.projectfields)
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


    def get(self):
        print 'get'
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
        
        
        
        print 'searchword=',searchword
        print 'offset=',offset
        print 'limit=',limit
        print 'order=',order
        
        print 'self.projectfields=',self.projectfields
        
#        ret = db.news.find_one()
        if searchword=='' or searchword=='{}':
            print 'searchword=null'
#sort({"createdAt":-1})       

            orderv = order.split(",")
            print 'orderv=',orderv
            sortlist=[]
            if order is not "":
                 print 'order sort'

                 for sortvalue in orderv:
                
                    if sortvalue.startswith("-"):
                        sortlist.append((sortvalue[1:],-1))
                    else:
                        sortlist.append((sortvalue,1))
                                  
            try: 
                ret= db[self.documentname].find({},projection=self.projectfields,skip=offset,limit=limit,sort=sortlist)
                
                
            except Exception,e:
                    print e
        else:
             dict = json.loads(searchword)
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
             sortlist=[]
             orderv = order.split(",")
             if order is not "":
                 print 'order sort'

                 for sortvalue in orderv:
                
                    if sortvalue.startswith("-"):
                        sortlist.append((sortvalue[1:],-1))
                    else:
                        sortlist.append((sortvalue,1))
                                  
             ret = db[self.documentname].find(dict,projection=self.projectfields,skip=offset,limit=limit,sort=sortlist)

#             orderv = order.split(",")
#             print 'orderv=',orderv
#             if order is not "":
#                 print 'order sort'
#                 for sortvalue in orderv:
                
#                    if sortvalue.startswith("-"):
#                         ret.sort(sortvalue[1:],-1)
#                    else:
#                        ret.sort(sortvalue)
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
            timestr= time.strftime('%Y-%m-%d %H:%M:%S')
            timestr =getIso8601()
            request.json['createdAt']=timestr
            if request.json.has_key("location"):
                    print 'find location'
                    location = request.json['location']
                    del location["__type"]
                    
            ret = db[self.documentname].insert(request.json)      
            print str(ret)
            retdict = {"objectId":str(ret),'createdAt':timestr}
            self.after_save(str(ret),"post");
#            return json.dumps(retdict),201
 #           client.close()
            return retdict
           
        except Exception,e:
            print e
        return "111"
class MResource(Resource):
    '''
    classdocs
    '''


    def __init__(self,documentname):
        '''
        Constructor
        '''
        self.documentname =documentname
    def after_put(self,objectid,putjson,action):
        print 'after_put1',objectid,putjson,action
    def get(self, todo_id):
        print 'MResource  get todo_id',todo_id
#        client = MongoClient(util.getMydbip())
        client = getMclient()
        db = client.test_database
#        abort_if_todo_doesnt_exist(todo_id)

#        return TODOS[todo_id]
        document = db[self.documentname].find_one({'_id': ObjectId(todo_id)})
        print 'document=',document
        if document==None:
                abort(404, message="{} doesn't exist".format(todo_id))
                    
#        return json.dumps(document,default=json_util.default)  
        oid =  str(document["_id"])
        del document["_id"]
        document['id']=oid
        document['objectId']=oid
            
        retstr = json.dumps(document,default=json_util.default)      
        print 'retstr=',retstr  
        newdict = json.loads(retstr)  

#       client.close()
        return newdict
    def delete(self, todo_id):
        print 'todo_id',todo_id
#        abort_if_todo_doesnt_exist(todo_id)
#        client = MongoClient(util.getMydbip())
        client = getMclient()
        db = client.test_database
        ret  = db[self.documentname].remove({'_id': ObjectId(todo_id)})   
        print 'ret=',ret   
#        client.close()  
        return {"code":200};

    def isOp(self,mydict):
            print 'mydict',mydict
            myitemlist = mydict.items()
            print 'myitemlist',myitemlist
            if len(myitemlist)==1:
                (key,value)= myitemlist[0]
                print 'key',key
                if isinstance(value, dict):
                    print 'isinstance'
                    if value.has_key("__op") and  value.has_key("objects"):
                            
                            op = value["__op"]
                            print 'op=',op
                            if op =='Add':
                                return ("$push",{key: value["objects"]})
            return None
    def put(self, todo_id):
        print "put=",request
        print 'todo_id',todo_id
        try:
 
#            newtodo_id = request.json['id'];
#            print "newtodo_id=",newtodo_id;

#           client = MongoClient(util.getMydbip())
            client = getMclient()
            try:
                del request.json["id"];
            except Exception,e:
                    print e
            db = client.test_database
            opword = request.args.get('op', '')
            print 'opword=',opword;
            dict1 = request.json
            if dict1.has_key("location"):
                     print 'location=',dict1['location']
                     mylocation = dict1['location']
                     del mylocation["__type"]

            
                             
            updatedAt= time.strftime('%Y-%m-%d %H:%M:%S')
            updatedAt =getIso8601()

            
            value = self.isOp(request.json)
            print 'value=,',value
            newdict = request.json
            if value is not None:
                (opword,newdict)=value
                print 'opword',opword
                print 'newdict',newdict
#            newdict['updatedAt']=updatedAt
            print 'newdict=',newdict
            if opword=='':
                print 'test1'
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{"$set":newdict})      
            else:
                
                ret = db[self.documentname].update({'_id': ObjectId(todo_id)},{opword:newdict,"$set":{'updatedAt':getIso8601()} }) 
            print 'ret=',ret
            retdict = {"id":todo_id,"updatedAt":updatedAt}
            self.after_put(todo_id,request.json,"put");
                
#            client.close()
            return retdict
#            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201

if __name__ == '__main__':
    pass