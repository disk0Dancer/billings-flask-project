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
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
    requisite_id = db.Column(db.Integer, db.ForeignKey('requisite.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    login = db.Column(db.String(50))
    password = db.Column(db.String(300))


    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != "id"}