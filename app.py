from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.requisite import Requisite
from models.invoice import Invoice

# import db_seed
# db_seed.seed()



@app.route('/')
def index():
    invoices = Invoice.query.all()
    return render_template('index.html', invoices=invoices)


@app.route('/requisites')
def requisites():
    requisites = Requisite.query.all()
    return render_template('requisite.html', requisites=requisites)


# method=['POST']
@app.route('/create_invoice'):
def create_invoice():
    pass


# method=['GET']
@app.route('/get_ivoice_status'):
def get_ivoice_status():
    pass


if __name__ == '__main__':
    app.run(debug=True)



