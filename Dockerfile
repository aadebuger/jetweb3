FROM    python:2
Add src/main/python /code
run pip install pingpp
run pip install flask
run pip install pymongo
run pip install mongoengine
run pip install flask_restful
run pip install passlib
run pip install qiniu
EXPOSE 5000
workdir /code
CMD ["python", "jetcloud/jetcloudrest.py"]
