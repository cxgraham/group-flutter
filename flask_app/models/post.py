from flask import flash
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import profile

class Post:
    db = 'flutter_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.content = data['content']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.profile_id = data['profile_id']
        self.creator = None

    
    # CREATE
    @classmethod
    def create_post(cls, data):
        # Add validate post method
        query = """
        INSERT INTO posts (name, content, location, profile_id)
        VALUES (%(name)s, %(content)s, %(location)s, %(profile_id)s)
        ;"""
        post_id = connectToMySQL(cls.db).query_db(query, data)
        print (post_id)
        return post_id


    # READ 
    @classmethod
    def get_all_posts(cls):
        query = """
        SELECT * FROM posts 
        LEFT JOIN profiles ON posts.profile_id = profiles.id
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        # print (results)
        all_posts = []
        for this_post in results:
            new_post = cls(this_post)
            this_creator = {
                'id': this_post['profiles.id'],
                'first_name': this_post['first_name'],
                'last_name': this_post['last_name'],
                'birthday': this_post['birthday'],
                'username': this_post['username'],
                'bio': this_post['bio'],
                'profilepic': this_post['profilepic'],
                'user_id': this_post['user_id'],
                'created_at': this_post['profiles.created_at'],
                'updated_at': this_post['profiles.updated_at']
            }
            new_post.creator = profile.Profile(this_creator)
            all_posts.append(new_post)
        return all_posts

    @classmethod
    def get_post_by_id(cls, id):
        data = {'id': id}
        query = """
        SELECT * FROM posts
        WHERE id = %(id)s
        ;"""
        this_post = connectToMySQL(cls.db).query_db(query, data)
        print (this_post)
        if this_post:
            this_post = cls(this_post[0])
        return this_post
    
    @classmethod
    def get_users_posts_by_id(cls, data):
        query = """
        SELECT * FROM posts
        LEFT JOIN profiles ON posts.profile_id = profiles.id 
        LEFT JOIN users ON profiles.user_id = users.id
        WHERE users.id = %(user_id)s
        ;"""
        users_posts = []
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        for post in results:
            users_posts.append(post)
        return users_posts



    # UPDATE
    @classmethod
    def edit_post_by_id(cls, data):
        # add validate post method
        query = """
        UPDATE posts
        SET content = %(content)s
        WHERE posts.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)


    # DELETE 
    @classmethod
    def delete_post_by_id(cls, id):
        data = {'id': id}
        query = """
        DELETE FROM posts
        WHERE posts.id = %(id)s
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    # VALIDATE