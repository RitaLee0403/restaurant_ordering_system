from flask import Flask, render_template, redirect, request, make_response
import jwt
import mysql_function 
import datetime
import time
from api import *

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
getData = mysql_function.ConnectToSql()


# Pages
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
	return render_template("thankyou.html")

app.register_blueprint(signup_api)
app.register_blueprint(attraction_api)
app.register_blueprint(categories_api)
app.register_blueprint(login_api)
app.register_blueprint(booking_api)


app.run(host = "0.0.0.0",port=3000,debug=True)

