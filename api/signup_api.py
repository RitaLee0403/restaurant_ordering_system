from flask import Blueprint ,  request
from models.signup import Signup
import re

signup_api = Blueprint("signup_api", __name__)
signup = Signup()

@signup_api.route("/api/user", methods = ["POST"])
def user():
	try:
		ok = {
			"ok" : True
		}
		data = request.json
		if(data["name"] == "" or data["email"] == "" or data["password"] == ""):
			return {
				"error" : True,
				"message": "任一項不可為空"
			},400
		emailRule =  re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
		if re.fullmatch(emailRule, data["email"]):
			if(not signup.is_email_registered(data["email"])):
				signup.signup(data["name"], data["email"], data["password"])
				return ok,200
			else:
						
				return {
					"error" : True,
					"message": "此email已經註冊過了"
				},400
		else:
			return {
				"error" : True,
				"message": "email格式錯誤"
			},400
	except:
		return {
			"error" : True,
			"message" : "伺服器出現錯誤"
		}