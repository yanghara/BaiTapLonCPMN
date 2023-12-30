from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum
from datetime import datetime


class UserRoleEnum(enum.Enum):
    PATIENT = 1
    DOCTOR = 2
    NURSE = 3
    ADMIN = 4


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    avatar = Column(String(150),
                    default='https://res.cloudinary.com/drv8vy8ww/image/upload/v1703861612/m2i3dxfctpt5dmmhxstd.png')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.PATIENT)
    # receipts = relationship('Receipt', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Medicine(db.Model):
    id = Column(String(5), primary_key=True)
    name = Column(String(150), nullable=False,unique=True)
    ngaysanxuat = Column(DateTime)
    hansudung = Column(DateTime, default=datetime.now())
    dongia = Column(Float, nullable=False, unique=True)


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())


# class Receipt(BaseModel):
#     user_id = Column(Integer, ForeignKey(User.id), nullable=True)
#     receipt_details = relationship('ReceiptDetails', backref='receipt', lazy=True)
#
#
# class ReceiptDetails(BaseModel):
#     quantity = Column(Float, default=0)
#     price = Column(Float, default=0)
#     receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
#     product_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        import hashlib

        u1 = User(name='MyVan', username='yanghara', password=str(hashlib.md5('abc123'.encode('utf-8')).hexdigest()),
                 user_role=UserRoleEnum.ADMIN)
        u2 = User(name='NhatThao', username='thaovu', password=str(hashlib.md5('18062003'.encode('utf-8')).hexdigest()),
                    user_role=UserRoleEnum.ADMIN)
        u3 = User(name='ThanhThuy', username='thuythuhai', password=str(hashlib.md5('24112003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.ADMIN)
        db.session.add_all([u1, u2, u3])
        db.session.commit()