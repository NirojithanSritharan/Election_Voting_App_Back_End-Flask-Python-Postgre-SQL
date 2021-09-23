from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# instantiate flask app
app = Flask(__name__)

# set configs of the app instance
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<User_name>:<Password>@<Host>/<Database_name>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# instatiate database object
db = SQLAlchemy(app)

# instatiate marshmallow object
ma = Marshmallow(app)

