from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_swagger_ui import get_swaggerui_blueprint
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import json

from app import app, db
from app.documentation import *
from app.models import *

# SWAGGER UI - https://localhost:5000/docs
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
# TODO create an HTML content body for all models

@app.route('/', methods=['GET'])
def hello():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('hello.html')


@app.route('/invoices', methods=['GET'])
@login_required
def index():

    if current_user.current_user().role != 'admin':
        flash('Доступ запрещен! Необходима роль: "admin"')
        return redirect(url_for('profile'))

    invoices = Invoice.query.order_by().all()
    invoices_list = [i.to_dict() for i in invoices]
    # print(invoices_list[0])
    return render_template('view.html', title="Заявки", data=invoices_list)


@app.route('/requisites')
@login_required
def requisites():
    requisites = Requisite.query.all()
    requisites_list = [i.to_dict() for i in requisites]
    # print(requisites_list[0])
    return render_template('view.html', title="Реквизиты", data=requisites_list)


@app.route('/users')
@login_required
def users():

    if current_user.current_user().role != 'admin':
        flash('Доступ запрещен! Необходима роль: "admin"')
        return redirect(url_for('profile'))

    users = User.query.all()
    users_list = [i.to_dict() for i in users]
    return render_template('view.html', data=users_list)


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
    args = dict(request.args)
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


@app.route('/login', methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":
        user = User.query.filter(User.login == request.form['login']).one()
        if user and check_password_hash(user.password, request.form['password']):

            userLogin = User().create(user)

            login_user(userLogin)

            flash("Выполнен вход.")
            return redirect(request.args.get('next') or url_for('index'))

        flash('Данные введены неверно!')

    return render_template('login.html')


@app.route('/registration', methods=["GET", "POST"])
def registration():

    if current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":

        is_exist =  User.query.filter(User.login == request.form['login']).count() > 0
        login_len = len(request.form['login']) > 4
        pwd_len = len(request.form['password']) > 4
        # current_user
        if (not is_exist) and pwd_len and login_len:
            id = User.query.count()+1
            pwd_hash = generate_password_hash(request.form['password'])
            new_user = User(id=id, login=request.form['login'], password=pwd_hash, role='user')

            db.session.add(new_user)
            db.session.commit()

            flash("Выполнена регистрация.")
        else:
            flash("Ошибка! Данный логин занят!")

        return redirect(url_for('login'))

    return render_template('registration.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()

    flash("Выполнен выход из профиля.")
    return redirect(url_for('login'))


@app.route('/profile', methods=["GET"])
@login_required
def profile():
    # print(current_user)
    return render_template('profile.html', current_user=current_user)