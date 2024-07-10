from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from school import school
from signup.models import UsersSignup
@school.route('/login',methods=["POST"])
def log():
    try:
        print(request.get_json())
        rs=request.get_json()
        user_first_name=rs.get("first_name")
        user_last_name=rs.get("last_name")
        mail=rs.get("email")
        username=rs.get("username")
        password=rs.get("pass")
        print(user_first_name)
        print(user_last_name)
        print(mail)
        print(username)
        print(password)
        UsersSignup(firstname=user_first_name,lastname=user_last_name,email=mail,username=username,password=password).save()
        return {"description":"login details","status":True,"status_code":200}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}

@school.route('/log_in',methods=["GET"])
def lst():
    try:
        data=UsersSignup.objects().to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"school datail","status":True,"data":newdata}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}