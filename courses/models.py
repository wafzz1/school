from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class coursedetails(Document):
    course_id=StringField(default="")
    course_name=StringField(default="")
    course_duration=StringField(default="")
    course_description=StringField(default="")
    course_fee=FloatField(default="")
class mapSchoolCourse(Document):
    school_id=StringField(default="")
    course_id=StringField(default="")