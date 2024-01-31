from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(50))
    login = db.Column(db.String(50))
    password = db.Column(db.String(100))

    def __init__(self, id, login, password, role):
        self.id = id
        self.role = role
        self.login = login
        self.password = hash(password)

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != "id"}