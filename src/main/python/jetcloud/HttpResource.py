'''
Created on 2015

@author: aadebuger
'''
import json

from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
import util
import MongoResource
import MongoAclResource

def getAcl(request):
    aclcondition = {}
    user = MongoAclResource.getObjectid(request)
    if user is None:
        return {}
    aclcondition = {'obarberid': user.obarberid}
    return aclcondition
def getResouce(database,documentname,request):
     
        print 'get'
        print 'message where=',request['where']
        client = MongoClient(util.getMydbip())
        db = client[database]
        print "list get=",request
        searchword = request.get('where', '')
        offset = int(request.get('offset', '0'))
        limit = int(request.get('limit', '0'))
        
        
        print 'searchword=',searchword
        print 'offset=',offset
        print 'limit=',limit
        
        
#        ret = db.news.find_one()
        if searchword=='' or searchword=='{}':
            print 'searchword=null'
#sort({"createdAt":-1})            
            try: 
                    if limit==0:
                        if offset ==0:
                            ret = db[documentname].find().sort([('_id', -1)])
                        else:
                            ret = db[documentname].find().sort([('_id', -1)]).offset(offset);
                    else:
                        if offset == 0 :
                            ret = db[documentname].find().sort([('_id', -1)]).limit(limit)
                        else:
                            ret = db[documentname].find().sort([('_id', -1)]).skip(offset).limit(limit)
            except Exception,e:
                    print e
        else:
             print 'searchword == dict'
#             dict = json.loads(searchword)
             dict = searchword
             if dict.has_key("objectId"):
                    oid = dict["objectId"]
                    dict['_id']=ObjectId(oid)
                    del dict["objectId"]
             print 'documentname=',documentname
             ret = db[documentname].find(dict)
        newsv = [];
        for news in ret:
            print 'news=',news
            print 'news get id',news.get("id")
            if news.get("id")==None:
                oid =  str(news["_id"])
                del news["_id"]
                news['id']=oid
            newsv.append(news)
        print 'newsv=',newsv
        retdict={}
        retdict['results']=newsv
#        return json.dumps(newsv,default=json_util.default)        
        retstr= json.dumps(retdict,default=json_util.default) 
        return retstr 
#        newdict = json.loads(retstr)  
#        return retdict
def postResource(documentname, request):
        print "post=",request
#      if not self.before_save():
#             return "111",404
        
        try:

            client = MongoClient(util.getMydbip())
            db = client.test_database

            timestr =MongoResource.getIso8601()
            request['createdAt']=timestr
            if request.has_key("location"):
                    print 'find location'
                    location = request['location']
                    del location["__type"]
            ret = db[documentname].insert(request)      
            print str(ret)
            retdict = {"objectId":str(ret),'createdAt':timestr}
#            self.after_save();
#            return json.dumps(retdict),201
            retstr= json.dumps(retdict,default=json_util.default) 
            return retstr 
        except Exception,e:
            print e
        return "111"


def putResource(documentname,request,todo_id):
        print "put=",request
        print 'todo_id',todo_id
        try:
#            print "put request=",request.json
#            newtodo_id = request.json['id'];
#            print "newtodo_id=",newtodo_id;
            client = MongoClient(util.getMydbip())
            try:
                del request["id"];
            except Exception,e:
                    print e
            opword = request.get('op', '')
            print 'opword=',opword;
            db = client.test_database


            updatedAt =MongoResource.getIso8601()
            request['updatedAt']=updatedAt
#            aclcondition = getAcl(request)
#            print 'aclcondition',aclcondition
            if opword=='':
                ret = db[documentname].update({'_id': ObjectId(todo_id)},{"$set":request})      
            else:
                ret = db[documentname].update({'_id': ObjectId(todo_id)},{opword:request}) 
            print 'ret=',ret
            retdict = {"id":todo_id,"updatedAt":updatedAt}
            retstr= json.dumps(retdict,default=json_util.default) 
            return retstr
#            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201
def deleteResource(documentname,request,todo_id):
        print "delete=",request
        print 'todo_id',todo_id
        try:
#            print "put request=",request.json
#            newtodo_id = request.json['id'];
#            print "newtodo_id=",newtodo_id;
            client = MongoClient(util.getMydbip())
            try:
                del request["id"];
            except Exception,e:
                    print e
            db = client.test_database

            ret  = db[documentname].remove({'_id': ObjectId(todo_id)})   

            return json.dumps({"code":200},default=json_util.default);
#            return json.dumps(retdict)
        except Exception,e:
            print e
        return "111",201
        
def parseRequest(database,documentname, request):
        print request.data
        newdict = json.loads(request.data)
        print 'newdict=',newdict
        try:
            method = newdict['_method']
            print 'method',method
        except Exception,e:
            method="POST"
        httpResource = { 'GET': lambda: getResouce(database,documentname,newdict),
            'POST': lambda: postResource(documentname,newdict),
 
          } 
        return httpResource[method]()
def parseRequestbydict(database,documentname, newdict):
#        print request.data
#        newdict = json.loads(request.data)
        print 'newdict=',newdict
        try:
            method = newdict['_method']
            print 'method',method
        except Exception,e:
            method="POST"
        httpResource = { 'GET': lambda: getResouce(database,documentname,newdict),
            'POST': lambda: postResource(documentname,newdict),
      
          } 
        return httpResource[method]()
    
def parseRequestbyid(documentname, request,oid):
        print request.data
        newdict = json.loads(request.data)
        print 'newdict=',newdict
        method = newdict['_method']
        print 'method',method

        httpResource = { 'GET': lambda: getResouce(documentname,newdict),
            'PUT': lambda: putResource(documentname,newdict,oid),
            'DELETE': lambda: deleteResource(documentname,newdict,oid), 
          } 
        return httpResource[method]()
if __name__ == '__main__':
    pass