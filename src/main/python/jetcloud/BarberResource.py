'''
Created on Aug 15, 2015

@author: aadebuger
'''
import json
from flask import Flask, request
#from flask.ext.restful import reqparse, abort, Api, Resource
from flask_restful import Resource, Api,abort
from pymongo import MongoClient
from pymongo import collection
#from pymongo import ReturnDocument


from pymongo import collection

from bson import json_util
from bson.objectid import ObjectId
import util
import time
from datetime import datetime
import MongodbOperation
from mongoengine import Document, EmailField, StringField, BooleanField, queryset_manager
from passlib.apps import custom_app_context as pwd_context
#from passlib.hash import pbkdf2_sha256
#from passlib.utils import consteq
from pymongo import read_preferences
import MongoResource
from jetuser import *


def newBarber(oshopid,phonenum,barbername ):
          client = MongoClient(util.getMydbip())

          db = client.test_database
          document = db["barber"].find_one({'phonenum': phonenum})
          print 'document=',document
          if document is not None:    
              print 'exist'  
              return False
          dict={};

          dict['oshopid']=oshopid
          dict['isreview'] =0      
          dict['phonenum']=phonenum
          dict['barbername']=barbername   
          dict['createdAt']=MongoResource.getIso8601()
          ret = db["barber"].insert(dict)  
          print 'newBarber=',ret
          return True
def reviewBarber(obarberid):
          client = MongoClient(util.getMydbip())

          db = client.test_database
          dict={};
          document = db["barber"].find_one({'_id': ObjectId(obarberid)})
          print 'document=',document
          updatedAt= MongoResource.getIso8601()
          
          if document==None:      
              return None
          ret = db["barber"].update({'_id': ObjectId(obarberid)},{"$set":{"isreview":1,"updatedAt":updatedAt}})
          print 'ret=',ret
          phonenum = document['phonenum']
          oshopid = document['oshopid']
          print 'phonenum=',phonenum
          user =User.objects.filter(username=phonenum).first()
          if user is not None:
                print 'user=',user
                user.oshopid=oshopid
                user.obarberid= obarberid
                user.save()
          else:
              print 'user=none'
          return updatedAt
              

if __name__ == '__main__':
    pass