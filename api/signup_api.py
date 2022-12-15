from flask import Blueprint ,  request
from api.models.signup import Signup

signup_api = Blueprint("signup_api", __name__)
signup = Signup()

@signup_api.route("/api/user", methods = ["POST"])
def user():
	try:
		ok = {
			"ok" : True
		}
		data = request.json
		if(signup.is_signup_success(data["email"])):
			signup.signup(data["name"], data["email"], data["password"])
			return ok,200
		else:
			
			return {
				"error" : True,
				"message": "此email已經註冊過了"
			},400

	except:
		return {
			"error" : True,
			"message" : "伺服器出現錯誤"
		}