from flask import Flask, render_template, redirect, request
from api import *
import jwt
import requests
from dotenv import load_dotenv
from api.models.booking import Booking
import os
import time, datetime
load_dotenv()

jwtKey = os.getenv("jwt_key")
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
Booking = Booking()
jwt_key = jwtKey


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

@app.route("/api/orders", methods = ["POST"])
def api_order():
	getId = request.cookies.get("token")	
	try:
		if(getId):
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			data = request.json
			order_data = {
				"prime": data["prime"],
				"partner_key":'partner_yeQLIuC301cXIaSzi9aSSyPRqSZ3LCjainndDtmPytc9rbMArcK1LIxB',
				"merchant_id":'mayonnaise0403_TAISHIN',
				"amount":data["order"]["price"],
				"details":data["order"]["contact"]["name"],
				"cardholder":{
					"phone_number":data["order"]["contact"]["phone"],
					"name":data["order"]["contact"]["name"],
					"email":data["order"]["contact"]["email"]
				}
			}
			product_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			headers = {'content-type': 'application/json', "x-api-key": 'partner_yeQLIuC301cXIaSzi9aSSyPRqSZ3LCjainndDtmPytc9rbMArcK1LIxB'}
			response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', headers=headers, json=order_data).json()
			status_code = response["status"]
			trip = data["order"]["trip"]
			if(status_code == 0):
				for i in range(len(data["order"]["trip"])):
					Booking.order(  product_number,
									getId,
									data["order"]["trip"][i]["attraction"]["id"],\
									trip[i]["time"],\
									trip[i]["date"],\
									data["order"]["contact"]["name"],\
									data["order"]["contact"]["email"],\
									data["order"]["contact"]["phone"] ,\
									data["order"]["price"]
								)
				response_data = {
					"data" : {
						"number" : product_number,
						"payment" : {
							"status" : status_code,
							"message" : response["msg"]
						}
					}
				}
				return response_data,200
			else:
				response_data = {
					"data" : {
						"number" : product_number,
						"payment" : {
							"status" : status_code,
							"message" : response["msg"]
						}
					}
				}
				return response_data,400
		else:
			return{
				"error":True,
				"message":"未登入"
			},403
	except:
		return {
			"error" : True,
			"message" : "伺服器內部錯誤"
		},500
  
@app.route('/api/orders/<orderNumber>', methods=['GET'])
def get_order(orderNumber): 
	getId = request.cookies.get("token")
	try:
		if(getId):
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			order_data = Booking.get_order_data(orderNumber)
			booking_data = Booking.get_booking_data(getId)
			trip = []
			attraction_data = {"attraction":{}}
			print(booking_data)
			for i in booking_data:
				attraction_data["attraction"]["id"] = i[0]
				attraction_data["attraction"]["name"] = i[1]
				attraction_data["attraction"]["address"] = i[2]
				attraction_data["attraction"]["image"] = i[3]
				attraction_data["date"] = i[4]
				attraction_data["time"] = i[5]
				trip.append(attraction_data)
				attraction_data = {"attraction":{}}


			data = {
			"data": {
				"number" : order_data[0][0],
				"price" : order_data[0][4],
				"trip" : trip,
				"contact" : {
					"name" :  order_data[0][1],
					"email" : order_data[0][2],
					"phone" : order_data[0][3]
				},
				"status" : 1
			}
			}
			return data,200
		else:
			return {
				"error" : True,
				"message" : "未登入"
			},403
	except:
		return{
			"error":True,
			"message" : "未登入系統，拒絕存取"
		},500
	
app.register_blueprint(signup_api)
app.register_blueprint(attraction_api)
app.register_blueprint(categories_api)
app.register_blueprint(login_api)
app.register_blueprint(booking_api)


app.run(host = "0.0.0.0",port=3000,debug=True)

