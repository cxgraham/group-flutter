from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL

class Friend:
    def __init__(self,data):
        self.idfriend = data['idfriend']
        self.user_id = data['user_id']