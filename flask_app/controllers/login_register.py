from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['post'])
def login():
    data = {'email' : request.form['email']}
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password.", "loginmessage")
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password.", "loginmessage")
        return redirect ('/')
    session['user_id'] = user_in_db.id
    return redirect ('/wardrobe')
    
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/process', methods = ['post'])
def process():
    data1 = {'email' : request.form['email']}
    user_in_db = User.get_user_by_email(data1)
    if user_in_db:
        flash("User already exists. Please use another email.", "error")
        return redirect ('/register')
    if not Register.validate(request.form):
        return redirect ('/register')
    data = Register.parsed_data(request.form)
    user_id = Register.new_user(data)
    session['user_id'] = user_id
    return redirect ('/newprofile')

@app.route('/newprofile')
def profile():
    return render_template ('newprofile.html')

@app.route('/createprofile', methods = ['post'])
def createprofile():
    if not Profile.validate(request.form):
        return redirect ('/newprofile')
    data = Profile.parsed_data(request.form)
    newprofile = Profile.new_profile(data)
    flash("Congrats! Get started by adding items. Then when you have a few begin making your outfit sets.", "congrats")
    return redirect ('/wardrobe')

@app.route('/myprofile')
def myprofile():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id' : session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    return render_template ('myprofile.html', userinfo =userinfo)

@app.route('/editprofile')
def editprofile():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id' : session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    return render_template ('editprofile.html', userinfo =userinfo)

@app.route('/editmyprofile', methods = ['post'])
def editmyprofile():
    if not Profile.validate(request.form):
        return redirect ('/editprofile')
    data = Profile.parsed_data(request.form)
    editedprofile = Profile.edit_my_profile(data)
    return redirect ('/myprofile')

#login-register-profile works!

@app.route('/wardrobe')
def wardrobe():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id' : session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    session['profile_id'] = userinfo.id
    return render_template ('wardrobe.html', userinfo =userinfo)


@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
