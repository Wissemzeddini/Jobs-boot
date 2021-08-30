from flask import Flask, render_template, url_for   
import mysql.connector
from Apps.scraping import *

app = Flask(__name__) 

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Jobs"
)
@app.route("/")                   
def index():
  mycursor = mydb.cursor()
  query = """ SELECT * from keejob """
  mycursor.execute(query)
  res = mycursor.fetchall()
  return render_template('index.html', data=res)

@app.route("/scraping")
def scrap():
  scraping_core()
  mycursor = mydb.cursor()
  query = """ SELECT * from keejob """
  mycursor.execute(query)
  res = mycursor.fetchall()
  return render_template('index.html', data=res)

@app.route("/del")
def delete():
  mycursor = mydb.cursor()
  query = """ delete from keejob where 1 """
  mycursor.execute(query)
  mydb.commit()
  query = """ SELECT * from keejob """
  mycursor.execute(query)
  res = mycursor.fetchall()
  return render_template('index.html', data=res)

if __name__ == "__main__":        
    app.run()  