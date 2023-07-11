from flask import Flask, render_template, redirect, request
from api import *
import jwt
from dotenv import load_dotenv
import os
load_dotenv()


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
jwt_key = os.getenv("jwt_key")



@app.route("/")
def index():	
	return render_template("index.html")

@app.route("/attraction/<id>")
def showAttraction(id):
	return render_template("attraction.html")
  
@app.route("/booking")
def booking():
	cookie = request.cookies.get("token")
	if(cookie):
		return render_template("booking.html")	
	return redirect("/")   
    
@app.route("/thankyou")
def thankyou():
	num = request.args.get("number",'')
	return render_template("thankyou.html",num = num)



	
app.register_blueprint(signup_api)
app.register_blueprint(attraction_api)
app.register_blueprint(categories_api)
app.register_blueprint(login_api)
app.register_blueprint(booking_api)
app.register_blueprint(orders_api)
app.register_blueprint(history_order_api)
app.register_blueprint(member_page_api)

app.run(host = "0.0.0.0",port=4000,debug=True)

