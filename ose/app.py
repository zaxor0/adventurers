from ose import *
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  htmlBody = rollChar('test') 
  return render_template("sheet.html", htmlBody=htmlBody)
