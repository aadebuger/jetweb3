'''
Created on 2015

@author: aadebuger
'''
import requests

def clientGet():
        url ='http://localhost:5000/1.1/classes/order?where={"userid":"5580f21ee4b035745ad26fd8"}&order=-createdAt&limit=4&skip=0'
        r = requests.get(url)
        print 'r=',r.text
def clientGet1():
        url ='http://localhost:5000/1.1/classes/order?where={"userid":"5580f21ee4b035745ad26fd8","status":0}&order=-createdAt&limit=4&skip=0'
        r = requests.get(url)
        print 'r=',r.text

def clientGet2():
        url ='http://localhost:5000/1.1/classes/hairstyle?where={"sex":1}'
        r = requests.get(url)
        print 'r=',r.text
def clientGet3():
        url ='http://localhost:5000/1.1/classes/hairstyle?where={"sex":1}'
        r = requests.get(url)
        print 'r=',r.text
def clientGet4():
        url ='http://localhost:5000/1.1/classes/collection?where={"userid":"5580f21ee4b035745ad26fd8"}'

        r = requests.get(url)
        print 'r=',r.text    
#
def searchShop():
        url ='http://localhost:5000/1.1/classes/shop?where={"objectId":"558f8535421aa90f0302dc51"}'

        r = requests.get(url)
        print 'r=',r.text    
          
if __name__ == '__main__':
     clientGet()
     clientGet1()
     clientGet2()
     clientGet3()
     clientGet4()
     searchShop()

     