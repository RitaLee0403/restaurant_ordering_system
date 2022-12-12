from flask import Blueprint, request
import jwt
import mysql_function 
import time
from dotenv import load_dotenv
import os
load_dotenv()

jwtKey = os.getenv("jwt_key")
booking_api = Blueprint("booking_api", __name__)
getData = mysql_function.ConnectToSql()
jwt_key = jwtKey


@booking_api.route("/api/booking", methods = ["POST"])
def apiBookingPost():
	try:
		getId = request.cookies.get("token")
		if(getId):
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			bookingData = request.json
			orderDate = bookingData["date"]
			orderYear = int(orderDate[0:4])
			orderMonth = int(orderDate[5:7])
			orderDay = int(orderDate[8:])
			localtime = time.localtime()
			year = int(time.strftime("%Y", localtime))
			month = int(time.strftime("%m", localtime))
			day = int(time.strftime("%d", localtime))
			if(orderYear < year):  #判斷是否預約到過去的日期
				return {"error":True, "message" : "日期輸入錯誤"},400
			elif(orderYear == year and orderMonth < month):
				return {"error":True, "message" : "日期輸入錯誤"},400
			elif(orderYear == year and orderMonth == month and orderDay < day):
				return {"error":True, "message" : "日期輸入錯誤"},400
			getData.booking(int(getId),bookingData)
			return {"ok" : True},200
		else:
			return {"error":True, "message" : "尚未登入"},403
	except:
		return {"error":True, "message":'伺服器內部錯誤'},500
	
	


@booking_api.route("/api/booking", methods = ["GET","DELETE"])
def apiBooking():
	if request.method == "GET":
		getId = request.cookies.get("token")
		if(getId): 
		
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			datas = getData.get_booking_data(getId)
			bookingDatas = {"data":[]
			}
			attraction = {"attraction":{}}
			prev = -1
			for data in datas:
				if(data[0] == prev):
					continue
				prev = data[0]
				attraction["attraction"]["id"] = data[0]
				attraction["attraction"]["name"] = data[1]
				attraction["attraction"]["address"] = data[2]
				attraction["attraction"]["image"] = data[3]
				attraction["date"] = data [4]
				attraction["time"] = data[5]
				attraction["price"] = data[6]
				bookingDatas["data"].append(attraction)
				attraction = {"attraction":{}}

			return bookingDatas 
		else:
			return {"error":True,"message" : "未登入系統，拒絕存取"},403
	if request.method == "DELETE":
		try:
			deleteData = request.json
			deleteData = deleteData["attractionId"]
			getId = request.cookies.get("token")
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			getData.delete_booking(getId, deleteData)
			return {"ok":True},200
		except:
			return {"error":True , "message" : "刪除失敗"},403

