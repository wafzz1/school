from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class studentdetails(Document):
    student_name=StringField(default="")
    student_gender=StringField(default="")
    student_age=IntField(default="")
    student_contact=LongField(default="")
    student_email=StringField(default="")
    student_address=StringField(default="")
class mapCourseStudent(Document):
    course_id=StringField(default="")
    student_id=StringField(default="")