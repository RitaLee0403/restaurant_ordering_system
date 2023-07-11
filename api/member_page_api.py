from flask import Blueprint ,  request, render_template, redirect
import jwt
import os
from dotenv import load_dotenv
from models.booking import Booking
from models.updatee_profile import UpdateProfile
from models.signup import Signup
load_dotenv()

member_page_api = Blueprint("member_page_api", __name__)
jwt_key = os.getenv("jwt_key")
Booking = Booking()
UpdateProfile = UpdateProfile()
Signup = Signup()


@member_page_api.route("/member_page")
def member_page():
	getId = request.cookies.get("token")
	if(not getId):
		return redirect("/")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	id = getId["data"]["id"]	
	name = getId["data"]["name"]
	email = getId["data"]["email"]
	return render_template("member.html",id=id, name = name, email = email) 

@member_page_api.route("/check_is_upload_headshot")
def headshot():
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	getId = getId["data"]["id"]	
	if(os.path.isfile(f"static/images/{getId}.png")):
		return {"ok" : True, "id" : getId},200
	else:
		return {"error": True},200




@member_page_api.route("/change_profile" , methods = ["POST"])
def change_profile():
	try:
		getId = request.cookies.get("token")
		getId = jwt.decode(getId, jwt_key, algorithms="HS256")
		getId = getId["data"]["id"]	
		data = request.json
		if("name" in data):
			UpdateProfile.update_name(data["name"],getId)
			return {"ok":True, "message":"更新成功"},200

		if(Signup.is_email_registered(data["email"]) == True):
			return {"error":True, "message":"email已經被註冊過了"},400
		UpdateProfile.update_email(data["email"],getId)
		return {"ok":True, "message":"更新成功"},200
	except:
		return {"error":True, "message":"內部伺服器發生錯誤"},500
    


@member_page_api.route("/upload_img", methods = ["POST"])
def upload_img():
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	getId = getId["data"]["id"]	
	image = request.files["photo"]
	image = image.stream.read()
	if(len(image) == 0):
		return redirect("/member_page")
	write_file(image,f"./static/images/{getId}.png") #儲存到static/images
	return redirect("/member_page")
	





def write_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)