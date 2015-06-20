'''
Created on 2015

@author: aadebuger
'''
import json

from pymongo import MongoClient
from bson import json_util
import util


def getResouce(documentname,request):
     
        print 'get'
        print 'message where=',request['where']
        client = MongoClient(util.getMydbip())
        db = client.test_database
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
def postResource(request):
    print 'post'
    
def parseRequest(documentname, request):
        print request.data
        newdict = json.loads(request.data)
        print 'newdict=',newdict
        method = newdict['_method']
        print 'method',method

        httpResource = { 'GET': lambda: getResouce(documentname,newdict),
            'POST': lambda: postResource(newdict),
          } 
        return httpResource[method]()
if __name__ == '__main__':
    pass