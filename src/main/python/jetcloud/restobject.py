# -*- coding: utf-8 -*-
"""
Created on Nov 14, 2015

@author: aadebuger
"""
import json
import iso8601
import types
from bson.objectid import ObjectId
def fixup(adict, k, v):
    for key in adict.keys():

        
        if key == k:
            
            adict[key] = v
        elif type(adict[key]) is dict:
            fixup(adict[key], k, v)
def fixupvalueold(adict, k, v):
    for key in adict.keys():

        value1 = adict[key]

#        print 'type',isinstance({},dict)
        print 'type=',type(value1) is dict
        if type(value1) is dict:
            print 'value=',value1
def fixupvalue(adict):
        for key in adict:
#            print 'key=',key
            value = adict[key]
            print 'value=',value
            if key =='objectId':
                    adict['_id']=ObjectId(adict['objectId'])
                    del adict['objectId']
                
            else:
                try:
                    print type(value) is list
                    for key1 in value:
                        print 'key1=',key1
                        value1= value[key1]
#                        print 'value1=',value1
                        try:
                            if value1.has_key('__type'):
                                typevalue = value1['__type']
                                if typevalue=='Date':
                                    print iso8601.parse_date(value1['iso'])
                                    value[key1]=value1['iso']
                        except Exception,e:
                            print 'e=',e
                except Exception,e:
                    print 'e=',e
def fixupcreatedvalue(value):

            for key1 in value:
#                    print 'key1=',key1
                    value1= value[key1]
#                    print 'value1=',value1
                    if value1.has_key('__type'):
                        typevalue = value1['__type']
                        if typevalue=='Date':
                            print iso8601.parse_date(value1['iso'])
                            value[key1]=value1['iso']

def rest2mongo(restdict):
        for key in  restdict:
#            print 'key=',key
            if key=='createdAt' or key =='fanlidate' or key =='updatedAt':
                value=restdict[key]
                fixupcreatedvalue(value)
            if key== "$and" or key== "$or":
                value = restdict[key]
                for item in value:
#                    print 'item=',item
                    fixupvalue(item)
def formatrest2mongo(restdict):
        for key in  restdict:
            print 'key=',key
            if key=='createdAt' or key =='fanlidate' or key =='updatedAt':
                value=restdict[key]
                restdict[key]=value['iso']
            else:
                value=restdict[key]

                print(isinstance(value, dict))
                if isinstance(value, dict):
                    print("dict")
                    formatrest2mongo(value)
if __name__ == "__main__":
    print "restobject"
    jsonstr1="""{"status":1}"""
    jsonstr="""{"status": {"$gte": 0}, "$and": [{"createdAt": {"$gte": {"__type": "Date", "iso": "2015-11-01T16:00:00.000Z"}}}, {"createdAt": {"$lte": {"__type": "Date", "iso": "2015-11-14T16:00:00.000Z"}}}]}"""
    jsonstr="""{"status": {"$gte": 0}, "createdAt": {"$gte": {"__type": "Date", "iso": "2015-11-01T16:00:00.000Z"},"$lte": {"__type": "Date", "iso": "2015-11-14T16:00:00.000Z"}}}"""
    jsonstr="""{"status": {"$gte": 0}, "createdAt": {"$gte": {"__type": "Date", "iso": "2015-11-01T16:00:00.000Z"},"$lte": {"__type": "Date", "iso": "2015-11-14T16:00:00.000Z"}}}"""
    jsonstr="""{"$and":[{"objectId":"57e0dd1da22b9d0061248912"}]}"""
    jsonstr="""{"mobilePhoneNumber":{"$exists":true},"updatedAt":{"$gte":{"__type":"Date","iso":"2016-11-14T07:17:55.000Z"}}}"""
    jsonstr="""{"type":"INFORMATION","status":"enabled","content":{"title":"年报炒作浪将起","url":"http://ac-3G47drEA.clouddn.com/8fc3d82fc146df31f379.html","updatedAt":{"__type":"Date","iso":"2016-11-15T13:21:59.287Z"},"summary":"随着三季报落幕，A股市场已经进入年报炒作阶段，。数据显示，目前共计有超1130家公司发布2016年年报业绩预告，其中113家公司预告，其年报净利增长下限至少翻番，其中42只个股净利润至少翻三番。","thumbnail":"http://ac-3G47drEA.clouddn.com/6294566f969d67d166d7.png"}}"""
    
    dict1 = json.loads(jsonstr)
    print "dict=",dict1
#    fixup(dict,"aa","bb")
    formatrest2mongo(dict1)
    print 'dict=',dict1