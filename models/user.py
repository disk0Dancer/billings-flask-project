from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    login = db.Column(db.String(50))
    password = db.Column(db.String(300))


    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != "id"}