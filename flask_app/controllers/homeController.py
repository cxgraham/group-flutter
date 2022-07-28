import profile
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app) 

from flask_app.models.user import User
from flask_app.models.register import Register
from flask_app.models.profile import Profile
from flask_app.models.post import Post


@app.route('/homepage') #direct to main page, need to add user id to the url
def main():
    if 'user_id' not in session:
        flash("Please log back in")
        return redirect ('/')
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data) #userinfor can be changed to profile info if you want
    session['profile_id'] = userinfo.id
    allPosts = Post.get_all_posts()
    return render_template ('homepage.html', userinfo=userinfo, allPosts=allPosts)

@app.route("/profile/<int:id>")
def viewOneProfile(id):
    id = {'id': id}
    profileinfo = Profile.get_one_profile_by_id(id)
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    print(id)

    # Why doesn't profileinfo call????????
    print(userinfo)
    print(profileinfo)
    return render_template("viewOneProfile.html", userinfo=userinfo, profileinfo=profileinfo)

@app.route("/profiles/search", methods=['POST'])
def search():
    if 'user_id' not in session:
            flash("Please log back in")
            return redirect ('/')
    query = {'searchQuery': request.form['searchQuery']} #this is perform soley to check for falseness
    searchResult = Profile.profile_search(query)
    if searchResult == False:
        return redirect('/homepage')
    searchQuery = request.form['searchQuery'] #if something exist, the search term is stored to send to the search page
    return redirect(url_for("search_result", searchQuery = searchQuery))

@app.route("/search_result/<searchQuery>") #searchterm appears in the url
def search_result(searchQuery): 
    if 'user_id' not in session:
            flash("Please log back in")
            return redirect ('/')
    query = {'searchQuery': searchQuery} #doing the same as above again, with the intent of geting results
    searchResult = Profile.profile_search(query)
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    print("@@@@@@@@@@@@@@@@@displayRoute!!!!!!!", searchResult)
    return render_template("search_result.html", searchResult=searchResult, userinfo=userinfo)




@app.route("/search_result/")
def noResults():
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    return render_template("noSearchResult.html", userinfo=userinfo)


@app.route("/explore")
def explore():
    data = {'user_id': session['user_id']}
    userinfo = Profile.get_profile_by_id(data)
    allProfiles = Profile.get_all_profiles()
    print(allProfiles)
    return render_template("explore.html", userinfo=userinfo, allProfiles=allProfiles)