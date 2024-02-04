from functools import wraps

from sqlalchemy import text
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


def admin_required(func):
    @wraps(func)
    def inside_f(*args,**kwargs):
        if current_user.current_user.role != 'admin':
            flash('Доступ запрещен! Необходима роль: "admin"')
            return redirect(url_for('profile'))
        return func(*args, **kwargs)
    inside_f.__name__ = func.__name__
    return inside_f


@app.route('/', methods=['GET'], endpoint='hello')
def hello():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('profile'))
    return render_template('hello.html')


@app.route('/invoices', methods=["GET", "POST"], endpoint='invoices')
@login_required
@admin_required
def index():

    if request.method == "POST":
        key = json.loads(request.data)['key']
        invoices = Invoice.query.order_by(key).all()
        invoices_list = list(map(Invoice.to_dict, invoices))

        return jsonify(invoices_list)
    else:
        invoices = Invoice.query.order_by().all()
        invoices_list = list(map(Invoice.to_dict, invoices))
        keys = {str(i): key for i, key in enumerate(invoices_list[0].keys())} # порядок столбцов

        return render_template('view.html', title="Заявки", data=invoices_list, keys=keys, url='/invoices')


@app.route('/requisites', methods=["GET", "POST"], endpoint='requisites')
@login_required
def requisites():

    if request.method == "POST":
        data = json.loads(request.data)
        key = data['key']
        prev_key = data['prevkey']

        if key == prev_key:
            requisites = Requisite.query.order_by(text(key + ' desc')).all()
        else:
            requisites = Requisite.query.order_by(key).all()

        requisites_list = list(map(Requisite.to_dict, requisites))
        return jsonify(requisites_list)
    else:
        requisites = Requisite.query.all()
        requisites_list = list(map(Requisite.to_dict, requisites))
        keys = {str(i): key for i, key in enumerate(requisites_list[0].keys())}

        return render_template('view.html', title="Реквизиты", data=requisites_list, keys=keys, url='/requisites')


@app.route('/users', methods=["GET", "POST"], endpoint='users')
@login_required
@admin_required
def users():

    if request.method == "POST":
        key = json.loads(request.data)['key']
        users = User.query.order_by(key).all()
        users_list = list(map(User.to_dict, users))

        return jsonify(users_list)

    else:
        users = User.query.all()
        users_list = list(map(User.to_dict, users))
        keys = {str(i): key for i, key in enumerate(users_list[0].keys())}# порядок столбцов

        return render_template('view.html', data=users_list, keys=keys, url='/users')


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
    new_id = Invoice.query.count()+1
    args = dict(request.args)
    try:
        options = {
            "id": new_id,
            "amount": int(args['amount']),
            "status": "ожидает оплаты",
            "requisite_id": int(args['requisite_id']),
        }
        invoice = Invoice(**options)
        print(invoice.to_dict())
        db.session.add(invoice)
        db.session.commit()
        return jsonify({'id': new_id}), 200
    except Exception as ex:
        return jsonify("Bad Request: " + str(ex)), 400


@app.route(f'/get_invoice_status',  methods=['GET'])
def get_invoice_status():
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

    if current_user and current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":

        try:
            user = User.query.filter(User.login == request.form['login']).one()
        except Exception as ex:
            print(ex)
            flash('Пользователь с таким логином не найден')
        else:
            if user and check_password_hash(user.password, request.form['password']):

                user_login = User().create(user)

                login_user(user_login)

                flash("Выполнен вход.")
                return redirect(request.args.get('next') or url_for('index'))

            flash('Неверный пароль!')

    return render_template('login.html')


@app.route('/registration', methods=["GET", "POST"])
def registration():

    if current_user and current_user.is_authenticated:
        return redirect(url_for('profile'))

    if request.method == "POST":

        is_exist = User.query.filter(User.login == request.form['login']).count() > 0
        login_len = len(request.form['login']) > 4
        pwd_len = len(request.form['password']) > 4

        if not is_exist:
            if pwd_len and login_len:
                id = User.query.count()+1
                pwd_hash = generate_password_hash(request.form['password'])
                new_user = User(id=id, login=request.form['login'], password=pwd_hash, role='user')

                db.session.add(new_user)
                db.session.commit()

                flash("Выполнена регистрация.")
            else:
                flash("Ошибка! Логин и пароль должны быть длиннее 4-х символов!")

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
    return render_template('profile.html', current_user=current_user)