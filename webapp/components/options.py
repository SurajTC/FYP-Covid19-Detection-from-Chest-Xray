from flask.helpers import url_for
from flask.templating import render_template
from werkzeug.utils import redirect

from app import db, Users, Requests, Results

User=None

def get_messages():
  messageList=Users.query.filter(Users.message.isnot(None)).order_by(Users.messagedate.desc()).all()
  return messageList

def set_ActiveUser(user):
  global User
  User=user

def home():
  if(User.superuser):
    return render_template('home.html', msgObj=get_messages(), user=User)
  else:
    return render_template('u_home.html', msgObj=get_messages(), user=User)


def explore():
  count,positive = 0,0
  data = Results.query.order_by(Results.resultdate.desc()).all()
  for d in data:
    count+=1
    if d.result == 'Covid-19 Positive':
      positive+=1
  if(User.superuser):
    return render_template("explore.html", data = data, count=str(count).zfill(3), positive=str(positive).zfill(3), negative=str(count-positive).zfill(3), msgObj=get_messages(), user=User)
  else:
    return render_template("u_explore.html", data = data, count=str(count).zfill(3), positive=str(positive).zfill(3), negative=str(count-positive).zfill(3), msgObj=get_messages(), user=User)

def predict():
  if(User.superuser):
    return render_template('predict.html', msgObj=get_messages(), user=User)
  else:
    return render_template('notfound.html')

def toUpdate(id):
  if(User.superuser):
    to_update = Results.query.get_or_404(id)
    return render_template('update.html', data=to_update, msgObj=get_messages(), user=User)
  else:
    return render_template('notfound.html')

def manage():
  if(User.superuser):
    requests=Requests.query.all()
    users=Users.query.filter(Users.id != User.id).all()
    return render_template('manage.html', requests=requests, users=users, msgObj=get_messages(), user=User)
  else:
    render_template('notfound.html')

def dashboard():
  if(User.superuser):
    return render_template('dashboard.html', msgObj=get_messages(), user=User)
  else:
    return render_template('u_dashboard.html', msgObj=get_messages(), user=User)


###################################################################################
def addUser(id, superuser):
  to_add = Requests.query.get_or_404(id)
  print(superuser)
  new_user = Users(username=to_add.username, password=to_add.password, email=to_add.email, superuser=True if superuser=="on" else False)
  try:
    db.session.add(new_user)
    db.session.delete(to_add)
    db.session.commit()
  except:
    return "User cannot be added"

  return redirect('/admin/manage')

def denyUser(id):
  to_deny = Requests.query.get_or_404(id)
  try:
    db.session.delete(to_deny)
    db.session.commit()
  except:
    return "Request cannot be denied"

  return redirect('/admin/manage')
  
def updateUser(id, superuser):

  try:
    to_update = Users.query.get_or_404(id)
    to_update.superuser=int(superuser)
    db.session.commit()
  except:
    return "User cannot be updated"

  return redirect('/admin/manage')

def removeUser(id):
  to_remove = Users.query.get_or_404(id)
  try:
    db.session.delete(to_remove)
    db.session.commit()
  except:
    return "User cannot be removed"

  return redirect('/admin/manage')


# update predicted Result

# add notfound page wherever necessary-done
# url navigation control-done
# user and admin home-done
# design settings page-done
# user remove -done
# message system-done
# post message-done
# update password-done


