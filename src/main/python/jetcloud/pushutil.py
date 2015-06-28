'''
Created on 2015

@author: aadebuger
'''
import jpush as jpush
import os
import logging
#from conf import app_key, master_secret
def pushAll():
        print 'pushAll'
        app_key=os.environ.get('JPUSH_APP_KEY',"09bc724caa75be2669ca7411")
        master_secret= os.environ.get('JPUSH_SECRET',"fe3dea5c60401e23c708cb5a")
        _jpush = jpush.JPush(app_key, master_secret)
        print '_push',_jpush
        push = _jpush.create_push()
        push.audience = jpush.all_
        push.notification = jpush.notification(alert="Hello, world!")
        push.platform = jpush.all_
        ret = push.send()
        print 'ret=',ret
def getTags():
        app_key=os.environ.get('JPUSH_APP_KEY',"09bc724caa75be2669ca7411")
        master_secret= os.environ.get('JPUSH_SECRET',"fe3dea5c60401e23c708cb5a")
        _jpush = jpush.JPush(app_key, master_secret)
        device = _jpush.create_device()
        device.get_taglist()
if __name__ == '__main__':
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
#        getTags();
        pushAll()