from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder='./static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

# from models.requisite import Requisite
# from models.invoice import Invoice
# import db_seed
# db_seed.seed()

from routes import *


if __name__ == '__main__':
    app.run(debug=True)



