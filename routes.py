from app import app, db
from documentation import *
from models.requisite import Requisite
from models.invoice import Invoice
from flask_swagger_ui import get_swaggerui_blueprint
from flask import render_template, request, jsonify
import json


# SWAGGER - https://localhost:5000/docs
SWAGGER_URL = '/docs'
API_URL = '/swagger'
swagger_ui_blueprint = get_swaggerui_blueprint(
   SWAGGER_URL,
   API_URL,
   config={
       'app_name': 'My App'
   }
)

app.register_blueprint(swagger_ui_blueprint)


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
    """
       ---
       post:
         summary: Create invoice
         parameters:
           - in: query
             schema: CreateInputSchema
         responses:
           200:
             description: OK, invoice_id
             content:
               application/json:
                 schema: CreateOutputSchema
           400:
             description: Bad Request
             content:
               application/json:
                 schema: ErrorSchema

       """
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
    """
       ---
       get:
         summary: Get invoice status by id
         parameters:
           - in: query
             schema: GetInputSchema
         responses:
           200:
             description: OK, invoice_status
             content:
               application/json:
                 schema: GetOutputSchema
           400:
             description: Bad Request
             content:
               application/json:
                 schema: ErrorSchema

       """
    # на входе id заявки, на выходе статус заявки
    args = dict(request.args)
    try:
        id = int(args['id'])
        status = Invoice.query.filter(Invoice.id == id).one().status
        return jsonify({"status": status}), 200
    except Exception as ex:
        return jsonify("Bad Request: " + str(ex)), 400



@app.route('/swagger')
def create_swagger_spec():
   return json.dumps(get_apispec(app).to_dict())

