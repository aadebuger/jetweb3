# -*- coding: utf-8 -*-
'''
Created on 2015年5月29日

@author: aadebuger
'''
from flask import Flask
from flask_restful import Resource, Api,request
import MongoResource
import json
import cloudfile
app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')
@app.route('/1.1/files/<path:filename>', methods=['POST'])
def save_upload(filename):

#    file = request.files['file']
#    print 'file=',file

#    if file and allowed_file(file.filename):
        print 'data len',len(request.data)
        
        mediaid = MongoResource.newUpload("media");                
#        filename = secure_filename(file.filename)
        print 'filename=',filename
#        mongo.save_file("%s.jpg"%(mediaid), request.files['file'])
  
        cloudfile.uploadfile(filename,request.data)
        url="http://7xjdvj.com1.z0.glb.clouddn.com/%s"%(filename)
        name=filename
        retdict= MongoResource.newBucketUpload("files", len(request.data), "jetcloud",url, name)

        print 'retdict=',retdict    
        return json.dumps(retdict);
        
#        abort(404, message="mimetype error")

class Store(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="story"
class StoreList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="story"
class GameScore(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="GameScore"
class GameScoreList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="GameScore"
class feedback(MongoResource.MResource):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="feedback"
class feedbackList(MongoResource.MResourceList):
    def __init__(self):
        '''
        Constructor
        '''
        self.documentname ="feedback"
api.add_resource(StoreList, '/store')
api.add_resource(Store, '/store/<string:story_id>')
api.add_resource(GameScoreList, '/1.1/classes/GameScore')
api.add_resource(GameScore, '/1.1/classes/GameScore/<string:todo_id>')
api.add_resource(feedbackList, '/1.1/classes/feedback')
api.add_resource(feedback, '/1.1/classes/feedback/<string:todo_id>')


if __name__ == '__main__':
    app.run(debug=True)