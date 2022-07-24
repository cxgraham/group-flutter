# from asyncio.windows_events import NULL
from flask import flash, request, session
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

db =  'flutter_schema' #temporary database name for now, actual name TBD

class Register:
    def __init__(self, data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']

    @classmethod #adds new user email and password to the database
    def new_user(cls, data):
        print("*******", data)
        query = """INSERT INTO users (email, password)
                VALUES (%(email)s, %(password)s);
                """
        user_id = connectToMySQL(db).query_db(query,data)
        print (user_id)
        session['user_id'] = user_id # set created user to session
        return user_id

    @staticmethod #user email and password validations
    def validate(newuser): #fix password validate: 1234567890 works
        is_valid = True
        #email null
        if len(newuser['email'])<1:
            flash("An email is required", 'error')
            is_valid = False
        #email
        if not EMAIL_REGEX.match(newuser['email']):
            flash("Invalid email address.", 'error')
            is_valid = False
        #password
        if len(newuser['password'])<8:
            flash("Password must be at least 8 characters.", 'error')
            is_valid = False
        if str.islower(newuser['password']) == True:
            flash("Password must contain at least one uppercase character.", 'error')
            is_valid = False
        if any([char.isdigit() for char in newuser['password']]) == False:
            flash("Password must contain at least one number.", 'error')
            is_valid = False
        if newuser['password'] != newuser['confirm_password']:
            flash("Passwords do not match. Please try again.", 'error')
            is_valid = False
        return is_valid

    @staticmethod 
    def parsed_data(data): #data parsed after validation to save into database
        parsed_data = {}
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data        


