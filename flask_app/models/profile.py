from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import date

db = 'flutter_schema' #official database name

class Profile:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.birthday = data['birthday']
        self.bio = data['bio']
        self.user_id = data['user_id']
        self.idfriend = data["idfriend"]

    @classmethod  #new profile maker 
    def new_profile(cls, data):
        print("*******", data)
        query = """INSERT INTO profiles (first_name, last_name, birthday, username, bio, user_id)
                VALUES (%(first_name)s, %(last_name)s, %(birthday)s, %(username)s, %(bio)s, %(user_id)s);
                """
        result = connectToMySQL(db).query_db(query,data)
        print (result)
        return result

    @classmethod #get user's profile
    def get_profile_by_id(cls, data):
        # print("*********", data) 
        query = """SELECT * from profiles
                    LEFT JOIN users on users.id = profiles.user_id 
                    WHERE users.id = %(user_id)s;"""
        # print("$$$$$$", query) 
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod #edit profile
    def edit_my_profile(cls,data):
        query = """UPDATE profiles SET first_name= %(first_name)s, last_name = %(last_name)s, birthday = %(birthday)s, username= %(username)s, bio = %(bio)s
                    WHERE id = %(user_id)s;""" #note: this is the profile ID passed through the userinfo obj in editprofile.html
        result = connectToMySQL(db).query_db(query,data)


    @staticmethod
    def validate(newuser):
        is_valid = True
        #first_name
        if len(newuser['first_name'])<1:
            flash("Please enter your first name.", 'profileerror')
            is_valid = False
        #last_name
        if len(newuser['last_name'])<1:
            flash("Please enter your last name.", 'profileerror')
            is_valid = False        
        #username
        if len(newuser['username'])<1:
            flash("Please enter your last name.", 'profileerror')
            is_valid = False        
        #birthday
        if (newuser["birthday"])=="":
            flash("Please enter your birthdate.", "profileerror")
            is_valid = False
        else: 
            if (date.fromisoformat(newuser['birthday'])) >= date.today():
                flash("Birthdate cannot be today or in the future.", "profileerror")
                is_valid = False
        return is_valid

    @staticmethod
    def parsed_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['username'] = data['username'] 
        parsed_data['birthday'] = data['birthday']
        parsed_data['username'] = data['username']
        parsed_data['bio'] = data['bio']
        parsed_data['user_id'] = data['user_id']
        return parsed_data


