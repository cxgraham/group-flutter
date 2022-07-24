from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models import user, profile, post

# CREATE 
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
    return render_template('edit_post.html', this_post = this_post)


# UPDATE 
@app.route('/posts/update', methods = ['POST'])
def update_post():
    data = {
        'id': request.form['post.id'],
        'name': request.form['name'],
        'content': request.form['content'],
        'location': request.form['location']
    }
    post.Post.edit_post_by_id(data)
    return redirect('/homepage')


# DELETE
@app.route('/posts/delete/<int:id>')
def delete_post():
    post.Post.delete_post_by_id(id)
    return redirect (request.referrer)