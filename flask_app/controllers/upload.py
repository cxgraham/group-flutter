from flask_app import app
# from flask_app.models import item
import os, imghdr
from flask import redirect, request, session, flash
from werkzeug.utils import secure_filename
from flask_app.models import profile

app.config['UPLOAD_EXTENSIONS'] = ['pdf', 'png', 'jpg', 'jpeg', 'gif', '.webp']
app.config['MAX_CONTENT_LENGTH'] = 2* 1024 * 1024 #2MB Max file size, can be more if you all want

def validate_image(stream): #more on this code here: https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask under Validating file contents
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/uploadprofilepic', methods=['POST'])
def upload_files():
    app.config['UPLOAD_PATH'] = 'flask_app/static/img/profile_pics' #upload path
    uploaded_file = request.files['profilepic'] #request.files is what the form uses instead of request.form
    filename = secure_filename(uploaded_file.filename) #filename is processed securely, see more at https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/
    # print("$$$$$$$$$$$", request.form)
    userid = session['user_id'] #this will get added in front of the file name as a
    # print("$$$$$$$$$", filename)
    if filename != '': #if there is a filename....
        filename = f'{userid}_{filename}' #added the user_id to the front of it
        file_ext = os.path.splitext(filename)[1] #splits filename for validation
        if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream): #validation check
            flash("Error: Invalid file. Allowable files include JPGS/JEPGS, PDF, PNG, GIF, and WEBP", "profilepic_upload")
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        print("Filepath is", os.path.join(app.config['UPLOAD_PATH'], filename))
        filepath = f'img/profile_pics/{filename}' #this creates the url that will go into the database
        flash("File uploaded", "profilepic_upload") #Success! flash message
        data = {
            'user_id' : userid,
            'profilepic' : filepath
        } #data to be passed into the method/SQL query
        profile.Profile.edit_profilepic_url(data)
    else:
        flash("Error: No file attached", "profilepic_upload")
        return redirect ('/editprofile')
    return redirect ('/editprofile')

