'''
Created on 2015

@author: aadebuger
'''
import pingpp
import os 
import time
from leancloud import Query
from leancloud import Object
from leancloud import GeoPoint
import leancloud

def processOrder(orderno,ordertype):
    orderc = Object.extend('order')
    query = Query(orderc)
    order = query.get(orderno)
    print 'order=',order
    if order is not None:
        print 'not None'
        print 'odertype=',ordertype
        if ordertype == 'charge.succeeded':
            print 'charge.succeeded ok'
            order.set("status",1)
            order.save()
    else:
        print 'order is none'
        
    
def processEvent(item):
    print 'item=',item
    print 'item data=',item['data']
    print 'item type =',item["type"]
    print 'item data order_no =',item['data']["object"]["order_no"]
    print 'item created=',item['created']
    print 'time created=',time.ctime(item['created'])
    processOrder(item['data']["object"]["order_no"],item["type"])
def processEvents(retv):
    
    map(lambda item:processEvent(item),retv)
def getEvents():
    pingpp.api_key = os.environ.get('PINGPP_APP_KEY',"sk_live_nMnwcL8fzWdhdiVltgi29YmY")
    ret = pingpp.Event.all()
    print 'has_more',ret['has_more']
    processEvents(ret['data'])

if __name__ == '__main__':
     leancloud.init("g0aeaj0c2j5iab43aj7e94ouwqsgvuw6x46986tcu7oaap4x","mkmi33s2skg7keg1s126xuzn2hoik464xsgjudq04d9bj927")
    
     getEvents();