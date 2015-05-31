# -*- coding: utf-8 -*-
'''
Created on 2014年9月27日

@author: aadebuger
'''
from pymongo import MongoClient 
from bson import json_util
from bson.objectid import ObjectId
from bson.code import Code
import util

def toDict(x,y):
        print 'x=',x
        print 'y=',y
        print 'y[category]=',y['category']
        x[y['category']]=y['count']
        return x
def groupDocument(document,key):
        client = MongoClient(util.getMydbip())
        db = client.test_database
        reducer = Code("""
              function(obj, prev){
                  prev.count++;
                }
                """)
        results = db[document].group(key={"category":1},condition={}, initial={"count": 0}, reduce=reducer)
        print 'results1=',results
        mydict = reduce(toDict,results,{})
        print 'mydict=',mydict
        return mydict
        
if __name__ == '__main__':
    pass
