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
        self.profilepic = data['profilepic']
        self.user_id = data['user_id']
        # self.idfriend = data["idfriend"] #experienced issues with idfriend and creating post, commenting out for now until friend feature is created


#///////////// CREATE ////////////////////
    @classmethod  #new profile maker 
    def new_profile(cls, data):
        print("*******", data)
        query = """INSERT INTO profiles (first_name, last_name, birthday, username, bio, user_id)
                VALUES (%(first_name)s, %(last_name)s, %(birthday)s, %(username)s, %(bio)s, %(user_id)s);
                """
        result = connectToMySQL(db).query_db(query,data)
        print (result)
        return result

#///////////// READ ////////////////////
    @classmethod #get user's profile
    def get_profile_by_id(cls, data):
        # print("*********", data) 
        query = """SELECT * from profiles
                    LEFT JOIN users on users.id = profiles.user_id 
                    WHERE users.id = %(user_id)s;"""
        # print("$$$$$$", query) 
        result = connectToMySQL(db).query_db(query,data)
        if result:
            result = cls(result[0])
        return result


    @classmethod
    def get_all_profiles(cls):
        query = """SELECT * from profiles;"""
        result = connectToMySQL(db).query_db(query)
        allProfiles = []
        for oneProfile in result:
            this_profile = cls(oneProfile)
            allProfiles.append(this_profile)
        return allProfiles
            


    @classmethod
    def get_one_profile_by_id(cls, id):
        data = id
        query = """
        SELECT * FROM profiles
        WHERE id = %(id)s
        ;"""
        this_profile = connectToMySQL(db).query_db(query, data)
        print (this_profile)
        if this_profile:
            this_profile = cls(this_profile[0])
        return this_profile

    @classmethod
    def profile_search(cls, data):
        print("**", data)
        query = """ SELECT * FROM profiles
                WHERE username = %(searchQuery)s;
        """
        all_results = []
        result = connectToMySQL(db).query_db(query,data)
        # print("@@@@@@@@@@@@@@@@@model_result", result)

        for this_result in result:
            user = cls(this_result)
            all_results.append(user)
        return all_results

#///////////// UPDATE ////////////////////
    @classmethod #edit profile
    def edit_my_profile(cls,data):
        query = """UPDATE profiles SET first_name= %(first_name)s, last_name = %(last_name)s, birthday = %(birthday)s, username= %(username)s, bio = %(bio)s
                    WHERE id = %(user_id)s;""" #note: this is the profile ID passed through the userinfo obj in editprofile.html
        result = connectToMySQL(db).query_db(query,data)


    @classmethod #edit profilepic url
    def edit_profilepic_url(cls,data):
        query = """UPDATE profiles 
        LEFT JOIN users on users.id = profiles.user_id 
        SET profilepic = %(profilepic)s
        WHERE users.id = %(user_id)s"""
        result = connectToMySQL(db).query_db(query,data)
        # print ("profilepic UPDATE result", result)

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
        parsed_data['bio'] = data['bio']
        parsed_data['user_id'] = data['user_id']
        return parsed_data


