from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from school import school
from schoolmng.models import schooldetail
import logging

# Initialize Flask app
app = Flask(__name__)
# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@school.route('/create/school',methods=["POST"])
def create():
    try:
        print(request.get_json())

         # Log the incoming JSON data
        logging.info('Received JSON data: %s', request.get_json())

        rs=request.get_json()
        school_name=rs.get("schoolname")
        school_address=rs.get("address")
        print(school_name)
        print(school_address)
        school_data=schooldetail(school_name=school_name,school_address=school_address).save()
        school_data.school_id=str(school_data.id)
        school_data.save()

        logging.info('School name: %s, School address: %s', school_name, school_address)

        return {"description":"school created","status":True}
    except Exception as e:
        # print(e)
        # traceback.print_exc()
        logging.error('Exception occurred: %s', e, exc_info=True)
        return {"description":str(e),"status":False,"status_code":304}


@school.route('/school',methods=["GET"])
def listsss():
    try:
        data=schooldetail.objects().to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"school datail","status":True,"data":newdata}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


@school.route('/school/update',methods=["POST"])
def update():
    try:
        rs=request.get_json()
        id=rs.get("id")
        school_name=rs.get("schoolname")
        data=schooldetail.objects(id=id).update(school_name=school_name)
        print(data)
        # newdata=json.loads(data)
        # print(newdata)
        
        return {"description":"updates successfully","status":True,"data":[]}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}