from flask_user import UserMixin

from app import db


class Requisite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_payment = db.Column(db.String(50))
    card_type = db.Column(db.String(50))
    owner_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    limit = db.Column(db.Float)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != "id"}


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    requisite_id = db.Column(db.Integer, db.ForeignKey('requisite.id'), nullable=False)

    requisite = db.relationship('Requisite', backref=db.backref('invoices', lazy=True))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(50),  nullable=False, unique=True)
    password = db.Column(db.String(300),  nullable=False)

    def from_db(self, user_id):
        self.__user = User.query.filter(User.id == user_id).one()
        return self

    def create(self, user):
        self.__user = user
        return self


    def get_id(self):
        return str(self.__user.id)

    def to_dict(self):
        return {c.name: str(getattr(self.__user, c.name)) for c in self.__user.__table__.columns}
