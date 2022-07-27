import profile
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile
from flask_app.models.post import Post


@app.route('/homepage') #direct to main page, need to add user id to the url
def main():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data) #userinfor can be changed to profile info if you want
    session['profile_id'] = userinfo.id
    allPosts = Post.get_all_posts()
    return render_template ('homepage.html', userinfo=userinfo, allPosts=allPosts)

@app.route("/profile/<int:id>")
def viewOneProfile(id):
    id = {'id': id}
    profileinfo = Profile.get_one_profile_by_id(id)
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    print(id)

    # Why doesn't profileinfo call????????
    print(userinfo)
    print(profileinfo)
    return render_template("viewOneProfile.html", userinfo=userinfo, profileinfo=profileinfo)

