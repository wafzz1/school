from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
from school import school
from courses.models import coursedetails,mapSchoolCourse
@school.route('/create/course',methods=["POST"])
def course():
    try:
        print(request.get_json())
        rs=request.get_json()
        course_name=rs.get("cname")
        course_duration=rs.get("duration")
        course_description=rs.get("description")
        course_fee=rs.get("fee")
        school_id=rs.get("school_id")
        course_data=coursedetails(course_name=course_name,course_duration=course_duration,course_description=course_description,course_fee=course_fee).save()
        course_data.course_id=str(course_data.id)
        course_data.save()
        print(course_data.to_json())
        mapSchoolCourse(school_id=school_id,course_id=str(course_data.id)).save()
        return {"description":"course details","status":True}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}


# listing the created courses
@school.route('/course/list',methods=["GET"])
def courselst():
    try:
        data=coursedetails.objects().to_json()
        newdata=json.loads(data)
        print(newdata)
        return {"description":"course datail","status":True,"data":newdata}
    except Exception as e:
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}

# @school.route('/school/course/list',methods=["POST"])
# def schoolcourselist():
#     try:
#         print(request.get_json())
#         rs=request.get_json()
#         school_id=rs.get("school_id")
#         data=mapSchoolCourse.objects(school_id=school_id).to_json()
#         data=json.loads(data)
#         # list=[]
#         for i in data:
#             a=i['course_id']
#             print(a)
#             newdata=coursedetails.objects(id=a).to_json()
#             newdata=json.loads(newdata)
#             print(newdata)
#             i["coursedata"]=newdata
#         return {"description":"course datail","status":True,"data":data}
#     except Exception as e:
#         traceback.print_exc()
#         return {"description":str(e),"status":False,"status_code":304}


# fetching and listing data using loop 
@school.route('/school/course/list', methods=["POST"])
def school_course_list():
    try:
        # Assuming 'request' is imported from Flask and contains JSON data
        rs = request.get_json()
        school_id = rs.get("school_id")
        
        # Retrieve list of school courses based on school_id
        data = mapSchoolCourse.objects(school_id=school_id).to_json()
        data = json.loads(data)
        
        # Iterate through each course in data and fetch course details
        for i in data:
            a = i['course_id']
            # Fetch details of the course using course_id
            coursedata = coursedetails.objects(id=a).to_json()
            coursedata = json.loads(coursedata)
            # Add fetched course details to the current course object
            i["coursedata"] = coursedata
        
        # Return the constructed response containing all course details
        return {"description": "course details", "status": True, "data": data}
    
    except Exception as e:
        traceback.print_exc()
        return {"description": str(e), "status": False, "status_code": 304}


# fetching and listing data without using loop
@school.route('/school/course/listing', methods=["POST"])
def school_course_listing():
    try:
        rs = request.get_json()
        school_id = rs.get("school_id")
        
        # Aggregate pipeline to join mapSchoolCourse and coursedetails
        pipeline = [
            {"$match": {"school_id": school_id}},
            {"$lookup": {
                "from": "coursedetails",  # Collection name of CourseDetails
                "localField": "course_id",
                "foreignField": "course_id",
                "as": "coursedata"
            }},
            {"$project": {
                "_id": 0,  # Exclude _id from the output
                "school_id": 1,
                "course_id": 1,
                "coursedata.course_name": 1,  # Include all fields from coursedata
                "coursedata.course_duration": 1,
                "coursedata.course_description": 1,
                "coursedata.course_fee": 1
            }}
        ]
        
        # Execute aggregation pipeline
        data = list(mapSchoolCourse.objects.aggregate(*pipeline))
        
        return jsonify({"description": "course details", "status": True, "data": data})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"description": str(e), "status": False, "status_code": 304})
