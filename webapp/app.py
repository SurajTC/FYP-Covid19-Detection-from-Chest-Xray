from enum import unique
import re
from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

import cv2
import os

from components.options import *
from components.emailservice import recover_password, send_verification, send_result
from components.codegen import random_string
from components.covid_stats import covid_stats_india
from components.decode_img import url_to_image
from components.prediction import predict_output

Result=None
ActiveUser=None
UpdatePatient=None

def clearGlobal():
  global Result, ActiveUser, UpdatePatient
  Result=None
  ActiveUser=None
  UpdatePatient=None

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///static/data/DATABASE_MASTER.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    superuser = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    lastactive = db.Column(db.DateTime, default=datetime.now())
    messagedate = db.Column(db.DateTime)
    message = db.Column(db.Text)

    def __repr__(self):
        return '<Users %r>' % self.id

class Requests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Requests %r>' % self.id

class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient = db.Column(db.String(10), unique=True, nullable=False)
    result = db.Column(db.String(8), nullable=False)
    covid = db.Column(db.Float, nullable=False)
    normal = db.Column(db.Float, nullable=False)
    imageurl = db.Column(db.String(100), nullable=False)
    resultdate = db.Column(db.DateTime, default=datetime.now())
    comments = db.Column(db.Text)

    def __repr__(self):
        return '<Results %r>' % self.id



@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@app.route('/')
def index():
  return render_template('landing.html')

@app.route('/login')
def login():
  clearGlobal()
  return render_template('login.html')

@app.route('/logout')
def logout():
  if not(ActiveUser == None):
    user = Users.query.get_or_404(ActiveUser.id)
    user.lastactive=datetime.now()
    try:
      db.session.commit()
    except:
      return "Unable to update LastActive"
  
  clearGlobal()
  return redirect(url_for('login'))

@app.route('/admin/<string:option>', methods=['POST', 'GET'])
def admin(option):
  if(not(ActiveUser == None) and (ActiveUser.superuser)):
    switcher={
      "home":home(),
      "explore":explore(),
      "predict":predict(),
      "manage":manage(),
      "dashboard":dashboard(),
    }
    return switcher.get(option, render_template('notfound.html'))
  else:
    return render_template('notfound.html')

@app.route('/user/<string:option>', methods=['POST', 'GET'])
def user(option):
  if(not(ActiveUser == None) and not(ActiveUser.superuser)):
    switcher={
      "home":home(),
      "explore":explore(),
      "dashboard":dashboard(),
    }
    return switcher.get(option, render_template('notfound.html'))
  else:
    return render_template('notfound.html')


@app.route('/authenticate', methods=['POST', 'GET'])
def authenticate():
  global ActiveUser
  if request.method=='POST':
    response={'status':False, 'message':None, 'superuser':False}

    username=request.json['username']
    password=request.json['password']
    
    user = Users.query.filter_by(username=username).first()
    
    if(user is None):
      response['message']="User Not Found"
    else:
      if not(user.password==password):
        response['message']= "Incorrect Password"
      else:
        ActiveUser=user
        set_ActiveUser(ActiveUser)
        response['status']=True
        response['message']= "Authentication Successful"
        if(ActiveUser.superuser):
          response['superuser']= True

    return jsonify(response)
  else:
    return "ERROR AUTH"

@app.route('/signup', methods=['POST', 'GET'])
def signup():
  if request.method=='POST':
    response={'status':False, 'message':None, 'code':None}

    username=request.json['username']
    email=request.json['email']
    nwpassword=request.json['nwpassword']
    repassword=request.json['repassword']
    
    user = Users.query.filter_by(username=username).first()
    pending = Requests.query.filter_by(username=username).first()
    
    if(user is not None) or (pending is not None):
      response['message']="This Username is taken, please try another one"
    else:
      user = Users.query.filter_by(email=email).first()
      pending = Requests.query.filter_by(email=email).first()

      if(user is not None) or (pending is not None):
        response['message']="This Email is taken, please try another one"
      else:
        if not(nwpassword==repassword):
          response['message']= "Passwords not Matching"
        else:
          code=random_string()
          sendObj = {'username':username, 'email':email, 'code':code}
          send_verification(sendObj)
          response['status'] = True
          response['message'] = f"A verification code is sent to {email}, Please verify"
          response['code'] = code

    return jsonify(response)
  else:
    return "ERROR SIGNUP"

@app.route('/pending', methods=['POST', 'GET'])
def pending():
  if request.method=='POST':
    response={'status':False, 'message':None}

    username=request.json['username']
    email=request.json['email']
    nwpassword=request.json['nwpassword']

    new_data = Requests(username=username, password=nwpassword, email=email)
    try:
      db.session.add(new_data)
      db.session.commit()
      response['status']=True
      response['message']= "Your Request has been sent to Admin, your account will activate on verification"
    except:
      return 'Data cannot be added'

    return jsonify(response)
  else:
    return "ERROR SIGNUP"

@app.route('/recover/<string:username>', methods=['POST', 'GET'])
def recover(username):
  response={'message':None}

  user = Users.query.filter_by(username=username).first()

  if(user is None):
    response['message']='User Not Found'
  else:
    userObj={"username":user.username, "password":user.password, "email":user.email}
    recover_password(userObj)
    response['message']='Recovery Password has been sent to your email address'

  return jsonify(response)


@app.route('/liveStats', methods=['POST', 'GET'])
def liveStats():
  response=covid_stats_india()
  return jsonify(response)



@app.route('/test', methods=['POST', 'GET'])
def test():
  global Result
  if request.method == 'POST':
    file =request.json['image'];
    img=url_to_image(file)
    cv2.imwrite('static/temp/temp.png', img)
    result = predict_output()
    Result = result
    return jsonify(result)

  else:
    return "ERROR"

@app.route('/save', methods=['POST', 'GET'])
def save():
  if request.method == 'POST':
    global UpdatePatient
    if UpdatePatient:
      patient=UpdatePatient
    else:
      patient=request.form['patient-id'].strip()
    result=Result["result"]
    covid=Result["covid"]
    normal=Result["normal"]
    image=cv2.imread('static/temp/temp.png')
    os.remove('static/temp/temp.png')
    imageurl=patient+'.png'
    comments=request.form['comment-box'].strip()
    email=request.form['email-id'].strip()

    print(patient, result, covid, normal, imageurl, comments)
    try:
      if UpdatePatient:
        to_update = Results.query.filter_by(patient=patient).first()
        to_update.result=result
        to_update.covid=covid
        to_update.normal=normal
        to_update.imageurl=imageurl
        to_update.resultdate=datetime.now()
        to_update.comments=comments[0:250]
        print("inside update")
        UpdatePatient=None
      else:
        to_add=Results(patient=patient, result=result, covid=covid, normal=normal, imageurl=imageurl, comments=comments[0:250])
        db.session.add(to_add)
        print("inside add")

      db.session.commit()
      print("commit")
      cv2.imwrite('static/data/images/'+imageurl, image)
      print("save")

    except:
      return "unable to write Image"

    print(type(email))
    if(len(email)):
      sendObj = {'result':result, 'covid':covid, 'normal':normal, 'email':email}
      send_result(sendObj)

    return explore()

  else:
    return "ERROR"

@app.route('/delete/<int:id>')
def delete(id):
    to_delete = Results.query.get_or_404(id)
    try:
        os.remove('static/data/images/'+to_delete.imageurl)
        db.session.delete(to_delete)
        db.session.commit()
        return redirect('/admin/explore')
    except:
        return 'Data Cannot be Deleted'

@app.route('/admin/update/<string:patient>', methods=['POST', 'GET'])
def update(patient):
    to_update = Results.query.filter_by(patient=patient).first()
    if request.method == 'POST':
      try:
          return redirect('/admin/explore')
      except:
          return 'Data Cannot be Deleted'

    else:
      global UpdatePatient
      UpdatePatient=to_update.patient
      return toUpdate(to_update.id)


@app.route('/manage/<string:option>/<int:id>', methods=['POST', 'GET'])
def manageUser(option, id):
    if request.method == 'POST':
      if option=="add":
        superuser=request.form['admin']
        return addUser(id, superuser)
      elif option=="update":
        superuser=request.form['role']
        return updateUser(id, superuser)

    else:
      if option=="deny":
        return denyUser(id)
      elif option=="remove":
        return removeUser(id)
      else:
        return "FAILED"


@app.route('/post/<string:option>/<id>', methods=['POST', 'GET'])
def post(option, id):
  # data=Users.query.filter_by(username=session['username']).first()
  print(type(option), type(id))
  response={'status':False, 'message':None}
  user=Users.query.get_or_404(id)
  if request.method=='POST':
    if(option=="add"):
      message=request.json["message"][0:150]
      print(message)
      try:
        user.message=message
        user.messagedate=datetime.now()
        db.session.commit()
        response['status']=True
        response['message']= "Message Posted"
        return jsonify(response)
      except:
        response['message']= "Unable to Post Message"
        return jsonify(response)

  else:
    if option=="delete":
      try:
        user.message=None
        user.messagedate=None
        db.session.commit()
        response['status']=True
        response['message']= "Post Deleted"
        return jsonify(response)
      except:
        response['message']= "Unable to Delete Post"
        return jsonify(response)


@app.route('/updatepassword', methods=['POST', 'GET'])
def updatepassword():
  to_update=Users.query.get_or_404(ActiveUser.id)
  response={'status':False, 'message':None}
  if request.method == 'POST':
    oldpassword=request.json['oldpassword']
    nwpassword=request.json['nwpassword']
    repassword=request.json['repassword']
    
    if not(oldpassword == to_update.password):
      response['message']="Incorrect Password"
    else:
      if not(nwpassword == repassword):
        response['message'] = "Password Not Matching"
      else:
        try:
          to_update.password=nwpassword
          db.session.commit()
        except:
          response['message'] = "Unable to Update Password"
          return jsonify(response)
        
        response['status'] = True
        response['message'] = "Password Updated Successfully"
    return jsonify(response)

  else:
      return "Not POST"



if __name__ == "__main__":
    app.run(debug=True)