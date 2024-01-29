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