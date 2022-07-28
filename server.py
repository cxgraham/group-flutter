from flask_app.controllers import login_register, posts, homeController, upload, friends
from flask_app import app


if __name__=="__main__":   
    app.run(debug=True, port = 5000)