from app.Models import Medicine, User
import hashlib
from app import app, db
from flask_login import current_user


def load_medicine():
    return Medicine.query.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# nó đều lấy cái khóa chính

def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()




