import json
import os.path
from app import app ,db
from app.Models  import Thuoc ,UserRoleEnum, User, ChiTietToaThuoc, PhieuKhamBenh,HoaDon
from flask_login import current_user
import hashlib
from sqlalchemy import func
from flask import current_app, session
from flask_login import user_logged_in


def count_thuoc(thuoc):
    total_amount, total_quantity = 0, 0

    if thuoc:
        for c in thuoc.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] + 1

    return {
        "total_amount": total_amount,
        "total_quantity": total_quantity
    }


def count_receipt(receipt):
    total_payment = 0

    if receipt:
        for i in receipt.values():
            total_payment = float(i['tienKham']) + float(i['tienThuoc'])

    return {
        "total_payment": total_payment
    }