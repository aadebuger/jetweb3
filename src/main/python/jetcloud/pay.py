__author__ = 'Lekton'

import pingpp
from flask import Flask,request,Response
import json
import random
import string
import os
import time
app = Flask(__name__)

from MongoResource import *
def processEvent(item):
    try:
            print 'item=',item
            
            print 'item data=',item['data']
#            print 'item type =',item["type"]
#            print 'item data order_no =',item['data']["object"]["order_no"]
#            print 'item created=',item['created']
#            print 'time created=',time.ctime(item['created'])
    except Exception,e:
        print 'e=',e
def processOrder( objectid,form):
      print 'objectid',objectid
      pushEvent("order", form)
    
@app.route('/webhook', methods=['post'])
def do_webhook():
    print 'data=',request.data
    print 'json data=',request.json

    processEvent(request.json)
    print 'json data data =',request.json['data']    

    return "ok"
    

@app.route('/pay', methods=['POST'])
def do_charge():
    print request.url
    form = request.get_json()
    print 'data=',request.data
    print form
    orderno = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    if isinstance(form, dict):
        form['order_no'] = orderno
        form['app'] = dict(id=os.environ.get('PINGPP_APP_ID',"123456"))
        form['currency'] = "cny"
        form['client_ip'] = "127.0.0.1"
        form['subject'] = "Your Subject"
        form['body'] = "Your Body"
        if form.has_key("objectId"):
            print 'form objectid = ',form['objectId']
            form['order_no'] = form['objectId']
            processOrder(form['objectId'],form)
            del form['objectId']
    print form
    pingpp.api_key = os.environ.get('PINGPP_APP_KEY',"123456")
    response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **form)
    print "Response_Charge: " + str(response_charge)
    return Response(json.dumps(response_charge), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,port=8888,host="0.0.0.0")