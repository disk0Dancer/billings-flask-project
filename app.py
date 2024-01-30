from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__, template_folder='./static/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost:5432/db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from models.requisite import Requisite
from models.invoice import Invoice
# import db_seed
# db_seed.seed()


@app.route('/', methods=['GET'])
@app.route('/invoices', methods=['GET'])
def index():
    # select = request.form.post('/sortBySelect')
    invoices = Invoice.query.order_by().all()
    return render_template('index.html', invoices=invoices)


@app.route('/requisites')
def requisites():
    requisites = Requisite.query.all()
    return render_template('requisite.html', requisites=requisites)


@app.route('/create_invoice',  methods=['POST'])
def create_invoice():
    # на входе тип реквизитов и сумма, на выходе id заявки и реквизиты
    id = Invoice.query.count()+1
    # print('id', id)
    args = dict(request.args)
    # print(args)
    try:
        options = {
            "id": id,
            "amount": int(args['amount']),
            "status": "ожидает оплаты",
            "requisite_id": int(args['requisite_id']),
        }
        invoice = Invoice(**options)
        print(invoice.to_dict())
        db.session.add(invoice)
        db.session.commit()
        return jsonify({'id': id}), 200
    except Exception as ex:
        return jsonify("Bad Request: " + str(ex)), 500


@app.route(f'/get_invoice_status',  methods=['GET'])
def get_ivoice_status():
    # на входе id заявки, на выходе статус заявки
    args = dict(request.args)
    try:
        id = int(args['id'])
        status = Invoice.query.filter(Invoice.id == id).one().status
        return jsonify({"status": status}), 200
    except Exception as ex:
        return jsonify("Bad Request: " + str(ex)), 404


if __name__ == '__main__':
    app.run(debug=True)



