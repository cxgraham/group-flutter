from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt   
from flask_app.models import profile, friend

bcrypt = Bcrypt(app) 
pw_hash = bcrypt.generate_password_hash('hunter2')
bcrypt.check_password_hash(pw_hash, 'hunter2') 

db = 'flutter_schema' #temporary database name for now, actual name TBD

class User:
    def __init__(self,data): #most user data is in proflie, which data ultimately goes to profile and user TBD
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        self.profile = []
        self.friends = []
        

    @classmethod
    def get_user_by_email(cls, data): #need for app.route(/login)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        print("THE result is", result)
        if len(result)<1:
            return False
        return cls(result[0])

    @classmethod 
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users LEFT JOIN profiles ON profiles.id = users.id WHERE users.id = %(id)s;"
        result = connectToMySQL(db).query_db(query, data)
        user = cls(result[0])
        for row in result:
            profile_data = {
                "id" : row['profiles.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "username" : row['username'],
                "birthday" : row['birthday'],
                "bio" : row['bio'],
                "profilepic" : row['profilepic'],
                "user_id" : row['user_id']
            }
            user.profile.append(profile.Profile(profile_data))
        return user

    #GET ALL USERS, FRINEDS OR NOT
    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM users LEFT JOIN profiles ON profiles.id = users.id WHERE users.id != %(user_id)s;"
        result = connectToMySQL(db).query_db(query, data)
        user = cls(result[0])
        for row in result:
            profile_data = {
                "id" : row['profiles.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "username" : row['username'],
                "birthday" : row['birthday'],
                "bio" : row['bio'],
                "profilepic" : row['profilepic'],
                "user_id" : row['user_id']
            }
            user.profile.append(profile.Profile(profile_data))
        return user 