from flask import Blueprint ,  request, redirect
from models.booking import Booking
import datetime
import requests
import jwt
from dotenv import load_dotenv
import os
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
load_dotenv()

orders_api = Blueprint("orders_api", __name__)
Booking = Booking()
jwtKey = os.getenv("jwt_key")
jwt_key = jwtKey
partner_key = os.getenv("partnerKey")
merchant_id = os.getenv("merchant_id")
jkopay_merchant_id = os.getenv("jkopay_merchant_id")
channel_id = os.getenv("channel_id")
channel_secret = os.getenv("channel_secret")
pwd = os.getenv("stmp_pwd")



@orders_api.route("/api/user_orders/<userId>", methods = ["GET"])
def api_user_orders():
    pass

@orders_api.route("/api/send_email", methods = ["POST"])
def api_send_email():
	try:
		# pdf_file_path = './files/output.pdf'
		# c = canvas.Canvas(pdf_file_path, pagesize=letter)
		# pdfmetrics.registerFont(TTFont('Roboto', "./font/Roboto-Black.ttf"))
		# c.setFont("Roboto", 12)
		# text = "這是一個測試的 PDF 文件。"
		# c.drawString(1 * inch, 10 * inch, text)
		# c.save()
		styles = getSampleStyleSheet()
		styleNormalCustom = ParagraphStyle(
			'styleNormalCustom',
			fontName='kaiu',
			parent=styles["Normal"],
			fontSize=30,
			leading = 20,
			alignment=TA_CENTER,
			spaceBefore = 20,
			spaceAfter = 30
		)

		
		message = ParagraphStyle(
			'styleNormalCustom',
			fontName='kaiu',
			parent=styles["Normal"],
			fontSize=15,
			leading = 20
		)
		# request.json["transactionId"]
		print(request.json)
		data = Booking.get_pdf_data(request.json["transactionId"])  

		pdfmetrics.registerFont(TTFont('kaiu', "./font/kaiu.ttf"))
		fileName = "./files/example.pdf"
		emailFileName = "example.pdf"
		pdfTemplate = SimpleDocTemplate(fileName)
		story = []
		story.append(Paragraph("親愛的" + data[0][5] + "您好，感謝您這次的購買。以下您所購買的行程明細。如果有任何問題歡迎回電。謝謝您。", message))
		story.append(Paragraph("訂單明細", styleNormalCustom))
		tableStyle = TableStyle([
			('ALIGN', (0, 0), (-1, -1), 'CENTER'), # 置中對齊
			('FONTNAME', (0, 0), (-1, -1), 'kaiu'), # 字體
			('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), # 上下置中
			("FONTSIZE", (0, 0), (5, 0), 15),
			('GRID', (0, 0), (-1, -1), 0.5, colors.black), # 框線黑色，寬度0.5
			('TOPPADDING', (0, 0), (-1, -1), 10),  # 設定上邊界的間距
			('BOTTOMPADDING', (0, 0), (-1, -1), 10),  # 設定下邊界的間距
			('LEFTPADDING', (0, 0), (-1, -1), 10),  # 設定左邊界的間距
			('RIGHTPADDING', (0, 0), (-1, -1), 10),  # 設定右邊界的間距
		])
		dataList = [
			["產品編號", "景點名稱", "日期", "時間", "價格"]
		]
		tempArr = []
		for i in data:
			tempArr.append(i[0])
			tempArr.append(i[2])
			tempArr.append(i[3])
			tempArr.append(i[4])
			if(i[4] == "morning"):
				tempArr.append("2000元")
			else:
				tempArr.append("2500元")
			dataList.append(tempArr)
			tempArr = []
		table = Table(dataList, style=tableStyle)
		story.append(table)
		pdfTemplate.build(story)
		msg = MIMEMultipart()
		with open(fileName, "rb") as file:
			filecontent=file.read()
		mime=MIMEApplication(filecontent)
		mime["Content-Type"]="application/pdf"  
		mime["Content-Disposition"]='attachment; fileName="' + emailFileName + '"'  
		mime["Subject"]="台北一日遊訂單確認通知"
		mime["From"]="台北一日遊客服中心"
		mime["To"]=data[0][5]
		# 副本收件者
		# email_body = "親愛的顧客您好，以下是您的消費明細資料。"
		# msg.attach(MIMEText(email_body, "plain"))
		mime["Cc"]="rita09436@gmail.com" 
		msg=mime.as_string() #將msg轉成str
		smtp=smtplib.SMTP("smtp.gmail.com", 587)  
		smtp.ehlo()
		smtp.starttls()
		smtp.login("rita09436@gmail.com", pwd) 
		from_addr="rita09436@gmail.com"
		to_addr=[data[0][6]]
		status=smtp.sendmail(from_addr, to_addr, msg)
		if status=={}:
			print("Email sent successfully!")
			smtp.quit()
			return {
				"status": "success"
			}
		
		print("Mail delivery failed!")
		smtp.quit()
		return {
			"status": "error"
		}
	except ZeroDivisionError as e:
    # 在這裡處理 ZeroDivisionError，並獲取錯誤代碼
		error_code = e.args[0]
		print(f"Error Code: {error_code}")
	

	

@orders_api.route("/api/linepay", methods = ["POST"])
def api_linepay():
	website_url = request.host_url
	product_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	getId = getId["data"]["id"]	
	order_price_arr = Booking.get_order_info(getId)
	print(order_price_arr)
	order_price = 0
	for i in order_price_arr:
		order_price += i[0]
	print(order_price)
	print("product_number" + product_number)
	order_price = int(order_price)
	order_data = {
		"amount": order_price,
		"currency": "TWD", 
		"productName": "行程總金額",
		"productImageUrl": "https://assets.thehansindia.com/h-upload/2022/07/18/1303611-pro.webp",
		"confirmUrl": website_url + 'thankyou?number='+ product_number + "&pay=linepay&price=" + str(order_price),
		"orderId": product_number
	}
	headers = {
		'content-type': 'application/json', 
		"X-LINE-ChannelId": channel_id, 
		"X-LINE-ChannelSecret": channel_secret
		}
	response = requests.post('https://sandbox-api-pay.line.me/v2/payments/request', headers=headers, json=order_data).json()
	print(response)
	print(response["info"]["paymentUrl"]["web"])
	return {"data" : response["info"]["paymentUrl"]["web"]}


@orders_api.route("/api/google/pay", methods = ["POST"])
def api_google_pay():
	website_url = request.host_url
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	userId = getId["data"]["id"]	
	userEmail = getId["data"]["email"]
	userName = getId["data"]["name"]
	data = request.json
	order_data = {
		"prime": data["prime"],
		"partner_key":partner_key,
		"merchant_id":merchant_id,
		"amount":data["order"]["price"],
		"details":"test",
		"cardholder":{
			"phone_number": "無",
			"name": userName,
			"email": userEmail
		}
	}
	product_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	headers = {'content-type': 'application/json', "x-api-key": partner_key}
	response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', headers=headers, json=order_data).json()
	status_code = response["status"]
	trip = data["order"]["trip"]
	if(status_code == 0):
		for i in range(len(data["order"]["trip"])):
			Booking.order(  product_number,
							userId,
							data["order"]["trip"][i]["attraction"]["id"],\
							trip[i]["time"],\
							trip[i]["date"],\
							userName,\
							userEmail,\
							"無" ,\
							data["order"]["price"]
						)
			

	response_data = {
		"data" : {
			"number" : product_number,
			"payment" : {
				"status" : status_code,
				"message" : response["msg"]
			}
		},
		"payment_url": website_url + 'thankyou?number='+ product_number + "&pay=googlepay&price=" + str(data["order"]["price"])
	}
	return response_data



@orders_api.route("/api/jkopay", methods = ["POST"])
def api_jkopay():
	website_url = request.host_url
	getId = request.cookies.get("token")
	getId = jwt.decode(getId, jwt_key, algorithms="HS256")
	userId = getId["data"]["id"]	
	userEmail = getId["data"]["email"]
	userName = getId["data"]["name"]
	data = request.json
	product_number = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
	order_price_arr = Booking.get_order_info(userId)
	order_price = 0
	for i in order_price_arr:
		order_price += i[0]
	order_price = int(order_price)
	order_data = {
				"prime": data["prime"],
				"partner_key":partner_key,
				"merchant_id":jkopay_merchant_id,
				"amount":data["order"]["price"],
				"details":userName,
				"cardholder":{
					"phone_number": "無",
					"name": userName,
					"email": userEmail
				},
				"result_url":{
					"frontend_redirect_url": website_url + 'thankyou?number='+ product_number + "&pay=jkopay&price=" + str(order_price),
					"backend_notify_url": "https://google.com"
				}
				
	}
	
	headers = {'content-type': 'application/json', "x-api-key": partner_key}
	response = requests.post('https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime', headers=headers, json=order_data).json()
	status_code = response["status"]
	trip = data["order"]["trip"]
	if(status_code == 0):
		for i in range(len(data["order"]["trip"])):
			Booking.order(  product_number,
							userId,
							data["order"]["trip"][i]["attraction"]["id"],\
							trip[i]["time"],\
							trip[i]["date"],\
							userName,\
							userEmail,\
							"無" ,\
							data["order"]["price"]
						)
	response_data = {
		"data" : {
			"number" : product_number,
			"payment" : {
				"status" : status_code,
				"message" : response["msg"]
			}
		},
		"payment_url": response["payment_url"]
	}
	return response_data,200


				
@orders_api.route("/api/jkopay/confirm", methods = ["POST"])
def api_jkopay_confirm():
	print(request.json)
	return {"status": "test"}

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
				"partner_key":partner_key,
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
			headers = {'content-type': 'application/json', "x-api-key": partner_key}
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
  