from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile


@app.route('/homepage') #direct to main page, need to add user id to the url
def main():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data) #userinfor can be changed to profile info if you want
    session['profile_id'] = session['user_id']
    return render_template ('homepage.html', userinfo = userinfo)