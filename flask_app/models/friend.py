from flask_app import app 
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import profile, user

class Friend:
    db = 'flutter_schema'
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.friend_id = data['friend_id']
        self.profiles = []

    # TO DO METHODS 
    '''
    GET LIST OF ALL FRIENDS TO USER (SHOW ALL FRIENDS)
    GET ONE FRIEND BY ID (SHOW FRIEND PAGE)
    GET ONE BY USERNAME (FIND FREIND BY USERNAME, OR SEARCH FRINEDS)
    JOIN FRIENDSHIP
    DELETE FRIENDSHIP 
    '''

    @classmethod
    def get_all_friends(cls, data):
        query = "SELECT * FROM friends LEFT JOIN profiles ON profiles.user_id = friends.friend_id WHERE friends.user_id = %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        friend = cls(result[0])
        for row in result:
            profile_data = {
                "id" : row['profiles.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "username" : row['username'],
                "birthday" : row['birthday'],
                "bio" : row['bio'],
                "profilepic" : row['profilepic'],
                "user_id" : row['profiles.user_id']
            }
            friend.profiles.append(profile.Profile(profile_data))
        return friend

    @classmethod
    def get_all_non_friends(cls, data):
        query = "SELECT * FROM friends LEFT JOIN profiles ON profiles.user_id = friends.friend_id WHERE friends.user_id != %(user_id)s AND friend_id != %(user_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        friend = cls(result[0])
        for row in result:
            profile_data = {
                "id" : row['profiles.id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "username" : row['username'],
                "birthday" : row['birthday'],
                "bio" : row['bio'],
                "profilepic" : row['profilepic'],
                "user_id" : row['profiles.user_id']
            }
            friend.profiles.append(profile.Profile(profile_data))
        return friend

    @classmethod
    def save_friendship(cls, data):
        query = "INSERT INTO friends (user_id, friend_id) VALUES (%(user_id)s, %(friend_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod
    def delete_friendship(cls, data):
        query = "DELETE FROM friends WHERE user_id = %(user_id)s AND friend_id = %(friend_id)s;"
        return connectToMySQL(cls.db).query_db(query, data)