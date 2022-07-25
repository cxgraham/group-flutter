from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL

class Friend:
    def __init__(self,data):
        self.idfriend = data['idfriend']
        self.user_id = data['user_id']

# TO DO METHODS 
'''
GET LIST OF ALL FRIENDS TO USER (SHOW ALL FRIENDS)
GET ONE FRIEND BY ID (SHOW FRIEND PAGE)
GET ONE BY USERNAME (FIND FREIND BY USERNAME, OR SEARCH FRINEDS)
JOIN FRIENDSHIP
DELETE FRIENDSHIP 
'''
