from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, profile, post

# CREATE
# Sam - Added create post rout 
@app.route('/posts/create', methods= ['GET'])
def create_post():
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    data = {'user_id' : session['user_id']}
    userinfo = profile.Profile.get_profile_by_id(data)
    print("***********SESSUIB PROFILE CHECK. SESSION PROFILE ID is ", session['profile_id'], "**********")

    return render_template('createpost.html', userinfo=userinfo)


@app.route('/posts/create', methods = ['POST'])
def add_post():
    if 'user_id' not in session:
        flash('You must create an account to add a post')
        return ('/register')
    post.Post.create_post(request.form)
    return redirect('/homepage')


# READ 
@app.route('/posts/edit/<int:id>')
def edit_post(id):
    this_post = post.Post.get_post_by_id(id)
    data = {'user_id' : session['user_id']}
    userinfo = profile.Profile.get_profile_by_id(data)
    return render_template('edit_post.html', this_post = this_post, userinfo = userinfo)


# UPDATE 
@app.route('/posts/update', methods = ['POST'])
def update_post():
    data = {
        'id': request.form['post.id'],
        'content': request.form['content'],
    }
    post.Post.edit_post_by_id(data)
    return redirect('/homepage')


# DELETE
@app.route('/posts/delete/<int:id>')
def delete_post(id):
    post.Post.delete_post_by_id(id)
    return redirect (request.referrer)