from flask import Blueprint, request, make_response
from api.models.login import Login
import jwt
import datetime
from dotenv import load_dotenv
import os
load_dotenv()

jwtKey = os.getenv("jwt_key")
login_api = Blueprint("login_api", __name__)
login = Login()
jwt_key = jwtKey


@login_api.route("/api/user/auth" , methods = ["GET", "PUT", "DELETE"])
def userAuth():
		ok = {
			"ok" : True
		}
		try:
			if request.method == 'PUT':
				data = request.json
				if(login.login(data["email"], data["password"])):
					userData = login.get_user_data(data["email"])
					response = make_response(ok)
					global payload_data
					payload_data = {
						"data" : {
						"id" : userData[0][0],
						"name" : userData[0][1],
						"email" : data["email"]
						}
					}
					token = jwt.encode(payload_data, jwt_key, algorithm="HS256")
					expire_date = datetime.datetime.now()
					expire_date = expire_date + datetime.timedelta(days=7)
					response.set_cookie("token", token,expires= expire_date)
					global initCookie
					initCookie = token
					return response, 200
				else:
					error = {
						"error" : True,
						"message" : "帳號或密碼錯誤"
					}
					return error,400
			if request.method == 'GET':
				cookie = request.cookies.get("token")
				#cookie 被改過的話要退出
				if(cookie and (initCookie == cookie)): 
					cookie = jwt.decode(cookie, jwt_key, algorithms="HS256")
					return cookie,200
				else:
					noneError = {
						"data" : None
					}
					
					return noneError,200
			if request.method == "DELETE":
				response = make_response(ok)
				response.delete_cookie("token")
				return response,200
		except:
			error = {
				"error" : True,
				"message" : "伺服器出現錯誤"
			}
			return error, 500
    