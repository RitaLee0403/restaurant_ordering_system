from flask import Blueprint ,  request
import mysql_function 

signup_api = Blueprint("signup_api", __name__)
getData = mysql_function.ConnectToSql()

@signup_api.route("/api/user", methods = ["POST"])
def user():
	try:
		ok = {
			"ok" : True
		}
		data = request.json
		if(getData.checkSignup(data["email"])):
			getData.addUserData(data["name"], data["email"], data["password"])
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