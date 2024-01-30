from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    status = db.Column(db.String(20))
    requisite_id = db.Column(db.Integer, db.ForeignKey('requisite.id'))

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
