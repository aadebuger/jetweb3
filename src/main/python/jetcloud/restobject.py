"""
Created on Nov 14, 2015

@author: aadebuger
"""
import json
import iso8601
import types
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
#            print 'value=',value
            try:
                print type(value) is list
                for key1 in value:
#                        print 'key1=',key1
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
            if key=='createdAt' or key =='fanlidate':
                value=restdict[key]
                fixupcreatedvalue(value)
            if key== "$and" or key== "$or":
                value = restdict[key]
                for item in value:
#                    print 'item=',item
                    fixupvalue(item)
if __name__ == "__main__":
    print "restobject"
    jsonstr1="""{"status":1}"""
    jsonstr="""{"status": {"$gte": 0}, "$and": [{"createdAt": {"$gte": {"__type": "Date", "iso": "2015-11-01T16:00:00.000Z"}}}, {"createdAt": {"$lte": {"__type": "Date", "iso": "2015-11-14T16:00:00.000Z"}}}]}"""
    jsonstr="""{"status": {"$gte": 0}, "createdAt": {"$gte": {"__type": "Date", "iso": "2015-11-01T16:00:00.000Z"},"$lte": {"__type": "Date", "iso": "2015-11-14T16:00:00.000Z"}}}"""

    dict = json.loads(jsonstr)
    print "dict=",dict
#    fixup(dict,"aa","bb")
    rest2mongo(dict)
    print 'dict=',dict