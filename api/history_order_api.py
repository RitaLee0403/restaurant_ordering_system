from flask import Blueprint ,  request, render_template, redirect
import jwt
import os
from dotenv import load_dotenv
from api.models.orders import Order
load_dotenv()

history_order_api = Blueprint("history_order_api", __name__)
jwt_key = os.getenv("jwt_key")
Order = Order()


@history_order_api.route("/history_order" )
def history_order():
	getId = request.cookies.get("token")
	if(not getId):
		return redirect("/")
	return render_template("history_order.html")



@history_order_api.route("/api/history_order" )
def api_history_order():
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	getId = getId["data"]["id"]	
	results = Order.get_history_order(getId)
	data = []
	attraction = {}
	trip = []
	information = {}
	count = 0
	last = len(results) - 1
	for result in results:
		if(count != 0):
			if(prev_product_num == result[0]):
				attraction["name"] = result[7]
				attraction["address"] = result[8]
				attraction["image"] = result[9]
				attraction["date"] = result[2]
				attraction["time"] = result[1]
				prev_product_num = result[0]
				trip.append(attraction)
				attraction = {}	
				if(count == last):
					information["attraction"] = trip
					data.append(information)
				count +=1
				continue
			else:
				information["attraction"] = trip
				data.append(information)
				trip = []
				information = {}	
		information["product_number"] = result[0] 
		prev_product_num = result[0]
		information["name"] = result[3]
		information["email"] = result[4]
		information["phone"] = result[5]
		information["price"] = result[6]
		information["attraction"] = []
		attraction["name"] = result[7]
		attraction["address"] = result[8]
		attraction["image"] = result[9]
		attraction["date"] = result[2]
		attraction["time"] = result[1]
		trip.append(attraction)
		attraction = {}
		if(count == last):
			information["attraction"] = trip
			data.append(information)
		count +=1
  

	return data,200
