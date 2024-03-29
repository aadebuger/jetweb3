# -*- coding: utf-8 -*-
__author__ = 'zhv'

import pingpp
from flask import Flask,request,Response
import json
import random
import string
import os
import time
import payevent
import leancloud
from celery import Celery
app = Flask(__name__)

from MongoResource import *

capp = Celery('smstasks', broker=os.environ.get('CELERY_BROKER_URL',"amqp://guest@localhost//"))
def processEvent(item):
    try:
            print 'item1=',item
            print 'item type =',item["type"]
            print 'item data order_no =',item['data']["object"]["order_no"]
            print 'item created=',item['created']
            print 'time created=',time.ctime(item['created'])
            payevent.processOrder(item['data']["object"]["order_no"],item["type"])
            
    except Exception,e:
        print 'e=',e
def processOrder( objectid,form):
      print 'objectid',objectid
#      pushEvent("order", form)
    
@app.route('/webhook', methods=['post'])
def do_webhook():
#    print 'data=',request.data
    newdict = json.loads(request.data)
    print 'newdict=',newdict
    print 'newdict data=',newdict["data"]
    
    dict1 = request.get_json()
    print 'json data4=',dict1
#    print 'item data=',request.json['data']
    if isinstance(dict1, dict):
        print 'is dict',
    else:
        print 'no dict',
    processEvent(newdict)
   

    return "ok"
    

@app.route('/pay', methods=['POST'])
def do_charge():
    print request.url
    form = request.get_json()
    print 'data=',request.data
    print form
    orderoid=''
#    orderno = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    uniqueid= util.__uniqueid__().next
    orderno =uniqueid()
    print 'orderno',orderno
    if isinstance(form, dict):
        form['order_no'] = orderno
        form['app'] = dict(id=os.environ.get('PINGPP_APP_ID',"123456"))
        form['currency'] = "cny"
        form['client_ip'] = "127.0.0.1"
        form['subject'] = "星范服务"
        form['body'] = "Your Body"
        if form.has_key("objectId"):
            print 'form objectid = ',form['objectId']
            orderoid= form['objectId']
            form['order_no'] = form['objectId']
            processOrder(form['objectId'],form)
            del form['objectId']
    print form
    pingpp.api_key = os.environ.get('PINGPP_APP_KEY',"123456")
    response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **form)
    print "Response_Charge: " + str(response_charge)
    payevent.updateOrder(orderoid,str(orderno),str(response_charge))
    
    return Response(json.dumps(response_charge), mimetype='application/json')

if __name__ == '__main__':

    leancloud.client.BASE_URL=os.environ.get("BASEURL",'https://api.leancloud.cn/1.1')
    leancloud.init("g0aeaj0c2j5iab43aj7e94ouwqsgvuw6x46986tcu7oaap4x","mkmi33s2skg7keg1s126xuzn2hoik464xsgjudq04d9bj927")
    capp.send_task('smscloud.smstasks.pushAll',args=["030701e583f","启动pay"],kwargs={})
    
    app.run(debug=True,port=8888,host="0.0.0.0")