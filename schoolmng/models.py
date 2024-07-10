from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
class schooldetail(Document):
    school_id=StringField(default="")
    school_name=StringField(default="")
    school_address=StringField(default="")