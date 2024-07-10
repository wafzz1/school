from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from school import school
from studentss.models import studentdetails,mapCourseStudent
@school.route('/create/student',methods=["POST"])
def student():
    try:
        print(request.get_json())
        rs=request.get_json()
        student_name=rs.get("name")
        student_gender=rs.get("gender")
        student_age=rs.get("age")
        student_contact=rs.get("contact")
        student_email=rs.get("email")
        student_address=rs.get("address")
        course_id=rs.get("course_id")
        print(student_name)
        print(student_gender)
        print(student_age)
        print(student_contact)
        print(student_email)
        print(student_address)
        student_data=studentdetails(student_name=student_name,student_gender=student_gender,student_age=student_age,student_contact=student_contact,student_email=student_email,student_address=student_address).save()
        print(student_data.to_json())
        mapCourseStudent(course_id=course_id,student_id=str(student_data.id)).save()
        return {"description":"student created","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# listing of students details
@school.route('/student_details',methods=["GET"])
def lists():
    try:
        data=studentdetails.objects().to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"school datail","status":True,"data":newdata}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}
        

# fetching the students
@school.route('/fetch/student',methods=["POST"])
def fetch():
    try:
        print(request.get_json())
        rs=request.get_json()
        course_id=rs.get("course_id")
        print(course_id)
        data=studentdetails.objects(id=course_id).to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"student details","status":True,"data":newdata}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# listing of a particular student
@school.route('/individual_student_details',methods=["POST"])
def listss():
    try:
        data=studentdetails.objects(student_name="sara").to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"school datail","status":True,"data":newdata}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# to update the detail
@school.route('/student/update',methods=["POST"])
def updated():
    try:
        rs=request.get_json()
        id=rs.get("id")
        student_name=rs.get("name")
        student_age=rs.get("age")
        student_email=rs.get("email")
        data=studentdetails.objects(id=id).update(student_name=student_name,student_age=student_age,student_email=student_email)
        print(data)
        return {"description":"updated successfully","status":True,"data":[]}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# to delete 
@school.route('/student/delete',methods=["POST"])
def delete():
    try:
        rs=request.get_json()
        id=rs.get("id")
        student_age=rs.get("age")
        data=studentdetails.objects(id=id, student_age=student_age).delete()
        print(data)
        # newdata=json.loads(data)
        # print(newdata)
        return {"description":"deleted successfully","status":True,"data":[]}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# to listout the students under a particular course
@school.route('/course/student/listing',methods=["POST"])
def course_student_listing():
    try:
        rs = request.get_json()
        course_id = rs.get("course_id")
        pipeline = [
            {"$match": {"course_id": course_id}},
            {"$lookup": {
                "from": "studentdetails", 
                "localField": "student_id",
                "foreignField": "student_id",
                "as": "studentdata"
            }},
            {"$project": {
                "_id": 0, 
                "course_id": 1,
                "student_id": 1,
                "studentdata.student_name": 1,  
                "studentdata.student_gender": 1,
                "studentdata.student_age": 1,
                "studentdata.student_contact": 1,
                "studentdata.student_email": 1,
                "studentdata.student_address": 1
            }}
        ]
        
       
        data = list(mapCourseStudent.objects.aggregate(*pipeline))
        
        return jsonify({"description": "student details", "status": True, "data": data})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"description": str(e), "status": False, "status_code": 304})
