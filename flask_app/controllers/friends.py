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
    return render_template("showfriends.html", friends=friend.Friend.get_all_friends(data), users=user.User.get_all_users(data))

@app.route("/friends/<int:id>")
def one_friend(id):
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {
        "id": id
    }
    data2 = {
        "user_id" : session['user_id']
    }
    return render_template("showfriend.html", user=user.User.get_user_by_id(data), friends=friend.Friend.get_all_friends(data2))

@app.route("/follow", methods=['POST'])
def save_friendship():
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {
        'user_id' : session['user_id'],
        'friend_id' : request.form['friend_id']
    }
    friend.Friend.save_friendship(data)
    return redirect("/friends")

@app.route("/unfollow", methods=['POST'])
def delete_friendship():
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {
        'user_id' : session['user_id'],
        'friend_id' : request.form['friend_id']
    }
    friend.Friend.delete_friendship(data)
    return redirect('/friends')