from models import *

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(app, model_class=Base)



with app.app_context():
    db.create_all()

    db.session.add(User(username="example"))
    db.session.commit()

    users = db.session.execute(db.select(User)).scalars()