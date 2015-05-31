FROM    python
Add src/python/main /code
EXPOSE 5000
CMD ["python", "jetcloud/jetcloudrest.py"]
