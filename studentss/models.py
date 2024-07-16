from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from signup.models import UsersSignup
class studentdetails(Document):
    firstname=StringField(default="")  
    lastname=StringField(default="")
    student_gender=StringField(default="")
    student_age=IntField(default="")
    student_contact=LongField(default="")
    student_email=StringField(default="")
    student_address=StringField(default="")
    student_id = StringField(default="")
    username=StringField(default="")
    password=StringField(default="")
    access_token=StringField(default="")
class mapCourseStudent(Document):
    course_id=StringField(default="")
    student_id=StringField(default="")