from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from app.config import *

# TODO change DB connection string
app = Flask(__name__, template_folder='../templates')
app.config['SQLALCHEMY_DATABASE_URI'] = db_connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super_secret_key'


db = SQLAlchemy(app)
migrate = Migrate(app, db)

loginManager = LoginManager(app)
loginManager.login_view = 'login'
loginManager.login_message = 'Необходимо войти в профиль.'
loginManager.login_message_category = 'success'


@loginManager.user_loader
def load_user(id):
    print('load_user')
    # print(User().from_db(id).to_dict())
    return User().from_db(id)


from app.routes import *
from app.db_seed import seed
seed()




