__author__ = 'Lekton'

import pingpp
from flask import Flask,request,Response
import json
import random
import string
import os
app = Flask(__name__)

from MongoResource import *
def processOrder( objectid,form):
      print 'objectid',objectid
      pushEvent("order", form)
    
@app.route('/webhook', methods=['post'])
def do_webhook():
    print 'webhook'

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
            processOrder(form['objectId'])
            del form['objectId']
    print form
    pingpp.api_key = os.environ.get('PINGPP_APP_KEY',"123456")
    response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **form)
    print "Response_Charge: " + str(response_charge)
    return Response(json.dumps(response_charge), mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,port=8888,host="0.0.0.0")