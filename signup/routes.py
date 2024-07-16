from flask import Flask,request,jsonify
from mongoengine import *
import traceback
import json
import datetime
from school import school
from flask_jwt_extended import *
from signup.models import UsersSignup

school.config["JWT_SECRET_KEY"] = "school22"  # Change this "super secret" to something else!
school.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
school.config['JWT_BLACKLIST_ENABLED'] = True
school.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(school)
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
        user=UsersSignup(firstname=user_first_name,lastname=user_last_name,email=mail,username=username,password=password).save() #creating and saving the user object
        access_token = create_access_token(identity=str(user.id)) #function (create_access_token) generates a JWT (JSON Web Token) access token
        user.access_token=access_token #Assigns the generated access token to the access_token attribute of the user object
        user.save()
        return {"description":"login details","status":True,"status_code":200,"access_token":access_token}
    except Exception as e:
        print(e)
        traceback.print_exc()
        return {"description":str(e),"status":False,"status_code":304}

@school.route('/login/credentials',methods=['POST'])    
def LoginCredentials():
    try:
        data=request.get_json()
        username=data['username']
        password=data['password']
        user=UsersSignup.objects(username=username,password=password).first()

        if user:
            print(user.id)
            # Generate JWT token
            access_token = create_access_token(identity=str(user.id))

            user.access_token = access_token
            user.save()

            # Prepare response with user details and JWT token
            response = {
                "status": True,
                "statuscode": 200,
                "data": [],  # Assuming to_dict() method exists in your model
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