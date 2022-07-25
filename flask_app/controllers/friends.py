from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.friend import Friend
from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile
from flask_app.models.post import Post

# Controllers
'''
Routes: /friends, /friend/<int:id>, /friend/username, /friend/unfollow, friend/follow
'''