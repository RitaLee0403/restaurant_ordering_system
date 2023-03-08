from flask import Blueprint ,  request
from models.booking import Booking
import datetime
import requests
import jwt
from dotenv import load_dotenv
import os
load_dotenv()

orders_api = Blueprint("orders_api", __name__)
Booking = Booking()
jwtKey = os.getenv("jwt_key")
jwt_key = jwtKey
partney_key = os.getenv("partnerKey")
merchant_id = os.getenv("merchant_id")


@orders_api.route("/api/user_orders/<userId>", methods = ["GET"])
def api_user_orders():
    pass


@orders_api.route("/api/orders", methods = ["POST"])
def api_order():
	getId = request.cookies.get("token")	
	try:
		if(getId):
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			data = request.json
			order_data = {
				"prime": data["prime"],
				"partner_key":partney_key,
				"merchant_id":merchant_id,
				"amount":data["order"]["price"],
				"details":data["order"]["contact"]["name"],
				"cardholder":{
					"phone_number":data["order"]["contact"]["phone"],
					"name":data["order"]["contact"]["name"],
					"email":data["order"]["contact"]["email"]
				}
			}
			product_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			headers = {'content-type': 'application/json', "x-api-key": partney_key}
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
				
				Booking.delete_all(getId)
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
  
@orders_api.route('/api/orders/<orderNumber>', methods=['GET'])
def get_order(orderNumber): 
	getId = request.cookies.get("token")
	try:
		if(getId):
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			order_data = Booking.get_order_data(orderNumber)
			booking_data = Booking.get_order_attraction_data(orderNumber)
			trip = []
			attraction_data = {"attraction":{}}
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
			"message" : "伺服器內部錯誤"
		},500
  