from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt   

bcrypt = Bcrypt(app) 
pw_hash = bcrypt.generate_password_hash('hunter2')
bcrypt.check_password_hash(pw_hash, 'hunter2') 

db = 'flutter_schema' #temporary database name for now, actual name TBD

class User:
    def __init__(self,data): #most user data is in proflie, which data ultimately goes to profile and user TBD
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        

    @classmethod
    def get_user_by_email(cls, data): #need for app.route(/login)
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        print("THE result is", result)
        if len(result)<1:
            return False
        return cls(result[0])