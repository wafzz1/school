from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from flask import Blueprint
dbs=connect(db='school', host='127.0.0.1', port=27017) #local
school = Flask(__name__)
# from course import routes
from schoolmng import routes
from studentss import routes
from signup import routes
from courses import routes
# student = Flask(__name__)
# @school.route('/smpl')
# def baseroute():
#     return "its working"


# class Grade(Document):
#     student_name=StringField(default="")
#     student_course=StringField(default="")
#     student_sem=StringField(default="")
#     student_grade=StringField(default="")

# @school.route('/grade',methods=["POST"])
# def grade():
#     try:
#         print(request.get_json())
#         rs=request.get_json()
#         student_name=rs.get("name")
#         student_course=rs.get("course")
#         student_sem=rs.get("sem")
#         student_grade=rs.get("grade")
#         Grade(student_name=student_name,student_course=student_course,student_sem=student_sem,student_grade=student_grade).save()
#         return {"description":"grade details","status":True}
#     except Exception as e:
#         print(e)
#         traceback.print_exc()
#         return {"description":str(e),"status":False,"status_code":304}

# @school.route('/grade/list',methods=["GET"])
# def gradlst():
#     try:
#         data=Grade.objects().to_json()
#         newdata=json.loads(data)
#         print(newdata)
#         return {"description":"course datail","status":True,"data":newdata}
#     except Exception as e:
#         traceback.print_exc()
#         return {"description":str(e),"status":False,"status_code":304}
















# @app.route('/list/user',methods=['GET'])
# def listuser():
#     try:
#         data=UsersSignup.objects().to_json()
#         newdata=json.loads(data)
#         response={}
#         response["status"]=True
#         response["statuscode"]=200
#         response["data"]=newdata
#         response['description']="successs"
#         return jsonify(response)
#     except Exception as e:
#         response={}    
#         response['status'] = False
#         response['status_code'] = 500
#         response['data'] = []
#         response['description'] = str(e)
#         return jsonify(response) 

if __name__ == "__main__":
    school.run()  