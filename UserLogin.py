from models import User


class UserLogin:

    def from_db(self, user_id):
        self.__user = User.query.filter(User.id == user_id).one()
        return self

    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user.id)

    def to_dict(self):
        return {c.name: str(getattr(self.__user, c.name)) for c in self.__user.__table__.columns}