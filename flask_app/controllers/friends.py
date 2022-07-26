from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import friend, user, profile

@app.route("/friends")
def all_friends():
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {
        "user_id" : session['user_id']
    }
    return render_template("showfriends.html", friends=friend.Friend.get_all_friends(data))

@app.route("/friends/<int:id>")
def one_friend(id):
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {
        "id": id
    }
    return render_template("showfriend.html", user = friend.Friend.get_friend_by_id(data))