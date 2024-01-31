from app import app, db
from models.invoice import Invoice
from models.requisite import Requisite
from models.user import User

from werkzeug.security import generate_password_hash, check_password_hash
import random
random.seed(0)


def seed():
    with app.app_context():
        db.create_all()

        names = ["Василий", "Иван", "Никита", "Валерий", "Антон", "Михаил", "Артур", "Даниил"]
        surnames = ["Иванов", "Петров", "Онянов", "Сидоров", "Клименко", "Максимов", "Болотов"]
        phones = ('8800800'+str(number) for number in range(1003,9999))

        for i in range(1, 101):
            options = {
                "id": i,
                "type_payment": random.choice(['карта', 'платежный счет']),
                "card_type": random.choice(['дебетовый', 'кредитный', 'овердрафтный', 'предоплаченый']),
                "owner_name": random.choice(names) + ' ' + random.choice(surnames),
                "phone_number": next(phones),
                "limit": random.randint(10000,1000000)
            }
            requisite = Requisite(**options)
            db.session.add(requisite)
            db.session.commit()

        for i in range(1, 5001):
            requisite_id = random.randint(1, 100)
            options = {
                "id": i,
                "amount": random.randint(123,9999),
                "status": random.choice(["ожидает оплаты", "оплачена", "отменена"]),
                "requisite_id": requisite_id,
            }
            invoice = Invoice(**options)
            db.session.add(invoice)
            db.session.commit()


        pwd_hash = generate_password_hash("admin")
        admin = User(id=1, login="admin", password=pwd_hash, role="admin")
        db.session.add(admin)
        db.session.commit()

        pwd_hash = generate_password_hash("user")
        user = User(id=2, login="user", password=pwd_hash, role="user")
        db.session.add(user)
        db.session.commit()