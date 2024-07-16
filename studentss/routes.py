from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
import datetime
from school import school
from flask_jwt_extended import *
# from signup.models import UsersSignup
from studentss.models import studentdetails,mapCourseStudent

school.config["JWT_SECRET_KEY"] = "school22"  # Change this "super secret" to something else!
school.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
school.config['JWT_BLACKLIST_ENABLED'] = True
school.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(school)

@school.route('/create/student',methods=["POST"])
def student():
    try:
        print(request.get_json())
        rs=request.get_json()
        user_first_name=rs.get("first_name")
        user_last_name=rs.get("last_name")
        student_gender=rs.get("gender")
        student_age=rs.get("age")
        student_contact=rs.get("contact")
        student_email=rs.get("email")
        student_address=rs.get("address")
        course_id=rs.get("course_id")
        student_id=rs.get("student_id")
        username=rs.get("username")
        password=rs.get("pass")
        # Assuming you have a way to identify the user who signed up, such as email or username
        # Fetch the user object
        # mail = rs.get("email")  # Assuming email is unique identifier
        # user = UsersSignup.objects(email=mail).first()

        print(user_first_name)
        print(user_last_name)
        print(student_gender)
        print(student_age)
        print(student_contact)
        print(student_email)
        print(student_address)
        print(username)
        print(password)
        student_data=studentdetails(firstname=user_first_name,
                                    lastname=user_last_name,
                                    student_gender=student_gender,
                                    student_age=student_age,
                                    student_contact=student_contact,
                                    student_email=student_email,
                                    student_address=student_address,
                                    student_id=student_id,
                                    username=username,
                                    password=password).save()# Linking student details to the user who signed up
        # student_data.course_id=str(student_data.id)
        # student_data.save()
        # print(student_data.to_json())
        mapCourseStudent(course_id=course_id,student_id=str(student_data.id)).save()
        access_token = create_access_token(identity=str(student_data.id)) #function (create_access_token) generates a JWT (JSON Web Token) access token
        student_data.access_token=access_token #Assigns the generated access token to the access_token attribute of the user object
        student_data.save()
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
        
# login
# @school.route('/login/credential',methods=['POST'])    
# def LoginCredential():
#     try:
#         data=request.get_json()
#         username=data['username']
#         password=data['password']
#         user=studentdetails.objects(username=username,password=password).first()

#         if user:
#             print(user.id)
#             # Generate JWT token
#             access_token = create_access_token(identity=str(user.id))

#             user.access_token = access_token
#             user.save()

#             # Prepare response with user details and JWT token
#             response = {
#                 "status": True,
#                 "statuscode": 200,
#                 "data": [],  # Assuming to_dict() method exists in your model
#                 "description": "successfully logged in",
#                 "access_token": access_token
#             }
#             return jsonify(response), 200
#         else:
#             response = {
#                 "status": False,
#                 "statuscode": 400,
#                 "data": [],
#                 "description": "invalid credentials"
#             }
#             return jsonify(response), 400
#     except Exception as e:
#         traceback.print_exc()
#         return {
#             "description": str(e),
#             "status": False,
#             "status_code": 304
#         }
@school.route('/login/credential', methods=['POST'])
def LoginCredential():
    try:
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = studentdetails.objects(username=username, password=password).first()

        if user:
            # Generate JWT token
            access_token = create_access_token(identity=str(user.id))

            # Save the access token to the user document
            user.access_token = access_token
            user.save()

            # Prepare response with user details and JWT token
            response = {
                "status": True,
                "statuscode": 200,
                "data": {
                    "firstname": user.firstname,
                    "lastname": user.lastname,
                    "student_gender": user.student_gender,
                    "student_age": user.student_age,
                    "student_contact": user.student_contact,
                    "student_email": user.student_email,
                    "student_address": user.student_address,
                    "student_id": user.student_id,
                    "username": user.username,
                    # Add more fields as needed
                },
                "description": "successfully logged in",
                "access_token": access_token
            }
            return jsonify(response), 200
        else:
            response = {
                "status": False,
                "statuscode": 400,
                "data": [],
                "description": "invalid credentials"
            }
            return jsonify(response), 400
    except Exception as e:
        traceback.print_exc()
        return {
            "description": str(e),
            "status": False,
            "status_code": 304
        }



# fetching the students by giving course_id
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


# fetching the students by student_id
@school.route('/fetch/students',methods=["POST"])
def fetching():
    try:
        print(request.get_json())
        rs=request.get_json()
        # student_id=rs.get("student_id")

        token = request.headers.get('Authorization')
        token = token.split()[1]  # Extract the token part after 'Bearer'
        decoded_token = decode_token(token)
        print(decoded_token)
        student_id = decoded_token['sub']
        print(student_id)
        data=UsersSignup.objects(id=student_id).to_json()
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
        data=studentdetails.objects(id=id).update(student_name=student_name,
                                                  student_age=student_age,
                                                  student_email=student_email)
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
        print(course_id)
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


# to listout the course under a particular student
@school.route('/student/course/listing',methods=["POST"])
def student_course_listing():
    try:
        rs = request.get_json()
        student_id = rs.get("student_id")
        # token = request.headers.get('Authorization')
        # token = token.split()[1]  # Extract the token part after 'Bearer'
        # decoded_token = decode_token(token)
        # print(decoded_token)

        # student_id = decoded_token['sub']  # Extract the 'sub' field from decoded token
        print(student_id)
        pipeline = [
            {"$match": {"student_id": student_id}},
            {"$lookup": {
                "from": "coursedetails", 
                "localField": "course_id",
                "foreignField": "course_id",
                "as": "coursedata"
            }},
            {"$project": {
                "_id": 0, 
                "student_id": 1,
                "course_id": 1,
                "coursedata.course_name": 1,  
                "coursedata.course_duration": 1,
                "coursedata.course_description": 1,
                "coursedata.course_fee": 1,
            }}
        ]
        
       
        data = list(mapCourseStudent.objects.aggregate(*pipeline))
        
        return jsonify({"description": "course details", "status": True, "data": data})
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({"description": str(e), "status": False, "status_code": 304})
