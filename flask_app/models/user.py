from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_bcrypt import Bcrypt   

bcrypt = Bcrypt(app) 
pw_hash = bcrypt.generate_password_hash('hunter2')
bcrypt.check_password_hash(pw_hash, 'hunter2') 

db = 'w2w'

class User:
    def __init__(self,data):
        self.id = data['id']
        self.email = data['email']
        self.password = data['password']
        

    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(db).query_db(query, data)
        print("THE result is", result)
        if len(result)<1:
            return False
        return cls(result[0])