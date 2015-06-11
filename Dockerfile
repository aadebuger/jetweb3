FROM    python:2
Add src/main/python /code
run pip install pingpp
run pip install flask
run pip install pymongo
run pip install mongoengine
EXPOSE 5000
workding /code
CMD ["python", "jetcloud/jetcloudrest.py"]
