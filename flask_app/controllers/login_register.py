from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile
from flask_app.models.post import Post


@app.route('/') #main login page
def index():
    return render_template('index.html')

@app.route('/login', methods = ['post']) #login processing route
def login():
    data = {'email' : request.form['email']} #data is used to check if email exists or not
    user_in_db = User.get_user_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password.", "loginmessage")
        return redirect ('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']): #password check
        flash("Invalid Email/Password.", "loginmessage")
        return redirect ('/')
    session['user_id'] = user_in_db.id #if everything good then user_id is in session for use in other places
    return redirect ('/homepage')
    
@app.route('/register') #registration page
def register():
    return render_template('register.html')

@app.route('/process', methods = ['post']) #registration processing route
def process():
    data1 = {'email' : request.form['email']}  #data is used to check if email exists or not
    user_in_db = User.get_user_by_email(data1)
    if user_in_db:
        flash("User already exists. Please use another email.", "error")
        return redirect ('/register')
    if not Register.validate(request.form): #validation check on registation info
        return redirect ('/register')
    data = Register.parsed_data(request.form)   #if validation is good proceed to save info and encrypt password
    user_id = Register.new_user(data) #SQL query when a new user is added returns the user's id, to then be passed into session
    session['user_id'] = user_id
    return redirect ('/createprofile')

@app.route('/createprofile') #create profile page
def profile():
    return render_template ('createprofile.html')

@app.route('/createnewprofile', methods = ['post']) #profile creation method
def createnewprofile():
    if not Profile.validate(request.form):
        return redirect ('/createprofile')
    data = Profile.parsed_data(request.form)
    newprofile = Profile.new_profile(data)
    return redirect ('/homepage') #direct to main page, need to add user id to the url

@app.route('/myprofile') #page for user to see their profile
def myprofile():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/') #userinfor can be changed to profile info if you want
    data = {'user_id' : session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    print("@@@@@@@@@@", userinfo)
    data = {'user_id' : session['user_id']}
    createdposts = Post.get_users_posts_by_id(data)
    return render_template ('myprofile.html', userinfo =userinfo, createdposts = createdposts)

@app.route('/editprofile') #edit profile page
def editprofile():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id' : session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    return render_template ('editprofile.html', userinfo =userinfo)

@app.route('/editmyprofile', methods = ['post']) #profile editing processing route
def editmyprofile():
    if not Profile.validate(request.form):
        return redirect ('/editprofile')
    data = Profile.parsed_data(request.form)
    editedprofile = Profile.edit_my_profile(data)
    return redirect ('/myprofile')

#login-register-profile works!


@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')
