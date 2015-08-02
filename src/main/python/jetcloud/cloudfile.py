# -*- coding: utf-8 -*-
'''
Created on 2015年5月31日

@author: aadebuger
'''
access_key='6oIzRgWr30MtIFhpngfaM6vY_9rpe4O9g0zb0KUT'
secret_key='4sU23mIWZzvFnHeXwB1uGnYNKZsj7u2KYF0nLEl6'
bucket_name="jetcloud"
import qiniu

import os
def get_bin_file(filename):
    '''
    Get the all content of the binary file.
    
    input: filename - the binary file name
    return: binary string - the content of the file. 
    '''

    if not os.path.isfile(filename):
        print("ERROR: %s is not a valid file." % (filename))
        return None

    f = open(filename, "rb")
    data = f.read()
    f.close()

    return data

def uploadfile(key,data):
    q = qiniu.Auth(access_key, secret_key)
#    key = 'hello'
#    data = 'hello qiniu!'
    token = q.upload_token(bucket_name)
    ret, info = qiniu.put_data(token, key, data)
    if ret is not None:
        print('All is OK')
        print 'ret=',ret
        print 'info=',info
        return ret
    else:
        print(info) # error message in info
def qiniuuploadfile(access_key1, secret_key1,bucket_name1,key,data):
    q = qiniu.Auth(access_key, secret_key)
#    key = 'hello'
#    data = 'hello qiniu!'
    token = q.upload_token(bucket_name1)
    ret, info = qiniu.put_data(token, key, data)
    if ret is not None:
        print('All is OK')
        print 'ret=',ret
        print 'info=',info
        return ret
    else:
        print(info) # error message in info
if __name__ == '__main__':
    pass