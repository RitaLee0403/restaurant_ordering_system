from flask import Flask, render_template, redirect, request
from api import *
import jwt
import requests
from dotenv import load_dotenv
import os
from models.booking import Booking
load_dotenv()


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
jwt_key = os.getenv("jwt_key")
channel_id = os.getenv("channel_id")
channel_secret = os.getenv("channel_secret")


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
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	getId = getId["data"]["id"]	
	num = request.args.get("number",'')
	pay = request.args.get("pay",'')
	transactionId = request.args.get("transactionId","")
	price = request.args.get("price","")
	if(pay == "linepay"):
		#linepay confirm api
		confirm_data = {
			"amount": int(price),
			"currency": "TWD"
		}
		headers = {
			'content-type': 'application/json', 
			"X-LINE-ChannelId": channel_id, 
			"X-LINE-ChannelSecret": channel_secret,
			"X-LINE-MerchantDeviceType": "POS",
			"X-LINE-MerchantDeviceProfileId": "DUMMY"
		}
		response = requests.post("https://sandbox-api-pay.line.me/v2/payments/" + transactionId + "/confirm", headers=headers, json=confirm_data).json()
		order_data = Booking().get_linepay_booking_data(getId)
		for i in order_data:
			Booking().order(num, getId, i[0], i[3], i[2], i[5], i[6], "無", price)
		# for i in order_data:
		# 	Booking().order()
		
	Booking().delete_all(getId)
	headers = {
		'content-type': 'application/json'
	}
	json = {
		"transactionId": num
	}
	url = "http://" + request.host + "/api/send_email"
	requests.post(url, headers = headers, json = json).json()
	return render_template("thankyou.html",num = num)

@app.route("/test")
def test():
	headers = {
		'content-type': 'application/json'
	}
	json = {
		"transactionId": "20221219175354"
	}
	url = "http://" + request.host + "/api/send_email"
	response = requests.post(url, headers = headers, json = json).json()
	return response
	
app.register_blueprint(signup_api)
app.register_blueprint(attraction_api)
app.register_blueprint(categories_api)
app.register_blueprint(login_api)
app.register_blueprint(booking_api)
app.register_blueprint(orders_api)
app.register_blueprint(history_order_api)
app.register_blueprint(member_page_api)

app.run(host = "0.0.0.0", port=4000, debug=True)

