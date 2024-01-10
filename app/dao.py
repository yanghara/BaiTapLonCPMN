from sqlalchemy import extract, func, distinct

from app.Models import *
import hashlib
from app import app, db
from flask_login import current_user
import cloudinary.uploader


def load_medicine():
    thuoc = db.session.query(Thuoc.id, Thuoc.name)

    return thuoc.all()


def load_benh_nhan():
    return [{
        'id': 1,
        'name': 'Đăng ký lịch khám'
    }]


def load_y_ta():
    return [{
        'id': 1,
        'name': 'Đăng ký lịch khám trực tiếp'
    }, {
        'id': 2,
        'name': 'Danh sách đăng ký khám'
    }]


def load_thu_ngan():
    return [{
        'id': 1,
        'name': 'Thanh toán hóa đơn'
    }]


def load_bac_si():
    return [{
        'id': 1,
        'name': 'Lập Phiếu Khám'
    }, {
        'id': 2,
        'name': 'Kê Toa Thuốc'
    }]


def load_patient():
    thuoc = db.session.query(BenhNhan.id, BenhNhan.ho, BenhNhan.ten, BenhNhan.ngay_sinh, BenhNhan.gioi_tinh,
                             BenhNhan.diachi, BenhNhan.so_dien_thoai)

    return thuoc.all()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# nó đều lấy cái khóa chính


def auth_user(username, password, type):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.user_role.__eq__(type.strip()),
                             User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def add_user(name, username, password, avatar, user_role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    u = User(name=name, username=username, password=password,
             avatar='https://cf.shopee.vn/file/1e1ed727b366712356405041c20c25ab',
             user_role=user_role)

    if avatar:
        res = cloudinary.uploader.upload(avatar)
        print(res)
        u.avatar = res['secure_url']

    db.session.add(u)
    db.session.commit()


def get_benh_nhan_by_id(bn_id=None):
    benhnhan = db.session.query(BenhNhan.id, BenhNhan.ho, BenhNhan.ten,
                                BenhNhan.gioi_tinh, BenhNhan.ngay_sinh, BenhNhan.diachi,
                                BenhNhan.email, BenhNhan.so_dien_thoai)
    if bn_id:
        benhnhan = benhnhan.filter(BenhNhan.id.__eq__(bn_id))

    return benhnhan.all()


def get_lich_su_benh(patient_id=None):
    query1 = (
        db.session.query(BenhNhan.id, BenhNhan.ho, BenhNhan.ten, BenhNhan.ngay_sinh,
                         BenhNhan.gioi_tinh, BenhNhan.email, BenhNhan.diachi, BenhNhan.so_dien_thoai,
                         PhieuKhamBenh.benh_nhan_id, PhieuKhamBenh.ngay_kham,
                         PhieuKhamBenh.trieu_chung, PhieuKhamBenh.du_doan_benh, BacSi.ho_ten, Thuoc.name,
                         DonViThuoc.ten)
        .join(PhieuKhamBenh, PhieuKhamBenh.bac_si_id.__eq__(BacSi.id))
        .join(BenhNhan, PhieuKhamBenh.benh_nhan_id.__eq__(BenhNhan.id))
        .join(ChiTietToaThuoc, ChiTietToaThuoc.phieu_kham_id.__eq__(PhieuKhamBenh.id))
        .join(Thuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id))
        .join(DonViThuoc, Thuoc.don_vi_thuoc_id.__eq__(DonViThuoc.id)))
    if id:
        query1 = query1.filter(PhieuKhamBenh.benh_nhan_id.__eq__(patient_id))

    return query1.all()


def get_thuoc(ten=None):
    query = ((db.session.query(Thuoc.id, Thuoc.name, DonViThuoc.ten, ChiTietToaThuoc.so_luong)
              .join(DonViThuoc, DonViThuoc.id.__eq__(Thuoc.don_vi_thuoc_id)))
             .join(ChiTietToaThuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id)))
    if ten:
        query = query.filter(Thuoc.name.contains(ten))

    return query.all()


def add_examination_form(**kwargs):
    benhnhan_id = kwargs.get('id')
    date = kwargs.get('date')
    symptom = kwargs.get('symptom')
    disease = kwargs.get('disease')
    medicineName = kwargs.get('medicineName')
    quantity = kwargs.get('quantity')
    unit = kwargs.get('unit')
    id = kwargs.get('id')
    instruction = kwargs.get('instruction')

    medicine = Thuoc.query.filter_by(name=medicineName).first()
    if medicine:
        idThuoc = medicine.id

    new_examination = PhieuKhamBenh(
        ngay_kham=date,
        trieu_chung=symptom,
        du_doan_benh=disease,
        benh_nhan_id=benhnhan_id,
        bac_si_id=id
    )
    db.session.add(new_examination)
    db.session.commit()

    if unit:
        donvi_thuoc = DonViThuoc.query.filter_by(id=unit).first()

    new_prescription = ChiTietToaThuoc(
        thuoc_id=idThuoc,
        phieu_kham_id=new_examination.id,
        so_luong=quantity,
        lieu_luong=donvi_thuoc.ten,
        cach_dung=instruction
    )
    db.session.add(new_prescription)
    db.session.commit()


def load_medicine2(kw=None):
    drugs = Thuoc.query.filter(Thuoc.id.isnot(None))

    if kw:
        drugs = drugs.filter(Thuoc.name.contains(kw))

    return drugs.all()


def check_thong_tin_benh_nhan(kw=None):
    patient = BenhNhan.query.filter_by(id=kw).first()
    if patient:
        patient = db.session.query(BenhNhan.ten)
    return patient.all()


def add_patient(info_patient):
    gioiTinh_mapping1 = {True: 'Nam', False: 'Nữ'}
    gioiTinh_string1 = gioiTinh_mapping1.get(info_patient['gioi_tinh'], 'Unknown')
    gioiTinh_boolean1 = 'Nam' if gioiTinh_string1 == 0 else 'Nữ'
    b = BenhNhan(ho=info_patient['ho'], ten=info_patient['ten'], \
                 ngay_sinh=info_patient['ngay_sinh'], gioi_tinh=0 if gioiTinh_boolean1 == 'Nam' else 1,
                 diachi=info_patient['diachi'], \
                 so_dien_thoai=info_patient['so_dien_thoai'])
    db.session.add(b)
    db.session.commit()


def add_receipt(info_receipt):
    if info_receipt:
        # for r in info_receipt:
        receipt = HoaDon()  # user=... => la backref
        # db.session.add(receipt)
        for info in info_receipt.values():
            gioiTinh_mapping = {True: 'Nam', False: 'Nữ'}
            gioiTinh_string = gioiTinh_mapping.get(info['gioiTinh'])
            gioiTinh_boolean = 'Nam' if gioiTinh_string == 0 else 'Nữ'
            d = ReceiptDetails(ho=info['ho'], ten=info['ten'], benhNhanId=info['benhNhanId'],
                               ngaySinh=info['ngaySinh'], gioiTinh=0 if gioiTinh_boolean == 'Nam' else 1,
                               diaChi=info['diaChi'],
                               ngayKham=info['ngayKham'], tienKham=info['tienKham'], tienThuoc=info['tienThuoc'],
                               tongTien=info['tongTien'],
                               hoadon=receipt
                               )
            db.session.add(d)
        db.session.commit()


def tan_suat_su_dung_thuoc(month):
    with app.app_context():
        # Tạo truy vấn cơ bản
        query = db.session.query(Thuoc.id, Thuoc.name,
                                 extract('month', PhieuKhamBenh.ngay_kham).label('Tháng'),
                                 (func.sum(ChiTietToaThuoc.so_luong) / 30 * 100).label('Tần suất sử dụng')
                                 ) \
            .join(ChiTietToaThuoc, ChiTietToaThuoc.thuoc_id.__eq__(Thuoc.id)) \
            .join(PhieuKhamBenh, PhieuKhamBenh.id.__eq__(ChiTietToaThuoc.phieu_kham_id)) \
            .group_by(Thuoc.name, extract('month', PhieuKhamBenh.ngay_kham))

        if month:
            query = query.filter(extract('month', PhieuKhamBenh.ngay_kham) == month)

        results = query.all()

        return results


def money_stats(month):
    with (app.app_context()):
        query = db.session.query(
            extract('month', HoaDon.created_date).label('Tháng'),
            func.sum(ReceiptDetails.tongTien).label('Doanh thu')
        ).join(ReceiptDetails, ReceiptDetails.receiptId.__eq__(HoaDon.id)
               ).group_by(extract('month', HoaDon.created_date))

        if month:
            query = query.filter(extract('month', HoaDon.created_date) == month)

        results = query.all()

        return results


def revenue_mon_stats(year=2024):
    query = db.session.query(HoaDon.created_date, func.extract('month', ReceiptDetails.ngayKham) \
                             , func.count((ReceiptDetails.benhNhanId)).label('patient_count')
                             , func.sum(ReceiptDetails.tongTien)) \
        .join(HoaDon, ReceiptDetails.receiptId.__eq__(HoaDon.id)) \
        .filter(func.extract('year', HoaDon.created_date).__eq__(year)) \
        .group_by(HoaDon.created_date, func.extract('month', ReceiptDetails.ngayKham))

    return query.all()


def receipt_detail_info(year, month):
    current_date = datetime.now()

    result = []

    for day in range(1, 32):
        query = db.session.query(
            HoaDon.id,
            ReceiptDetails.ngayKham,
            extract('month', HoaDon.created_date).label('Tháng'),
            func.count(ReceiptDetails.benhNhanId).label('patient_count'),
            func.sum(ReceiptDetails.tongTien).label('total_revenue')
        ).join(HoaDon, HoaDon.id == ReceiptDetails.receiptId) \
            .filter(
            func.extract('year', ReceiptDetails.ngayKham) == year,
            func.extract('month', ReceiptDetails.ngayKham) == month,
            func.extract('day', ReceiptDetails.ngayKham) == day

        ).group_by(HoaDon.id,ReceiptDetails.ngayKham)

        if month:
            query = query.filter(extract('month', HoaDon.created_date) == month)


        result.extend(query.all())

    return result


def tan_suat_kham(month):
    with (app.app_context()):
        # Tạo truy vấn cơ bản
        query = db.session.query(DanhSachKham.id,
                                 extract('month', DanhSachKham.ngay_kham).label('Tháng'),
                                 (func.sum(DanhSachKham.so_benh_nhan)),
                                 (func.sum(DanhSachKham.so_benh_nhan) / 30 * 100).label('Tần suất khám')
                                 ).group_by(DanhSachKham.id, extract('month', DanhSachKham.ngay_kham))

        if month:
            query = query.filter(extract('month', DanhSachKham.ngay_kham) == month)

        results = query.all()

        return results



def add_patient_onl(phieu):
    # if phieu:
    #     dsach = DanhSachKham()  # user=... => la backref
    #     # db.session.add(dsach)
    #     for info in phieu.values():
    gioiTinh_mapping1 = {True: 'Nam', False: 'Nữ'}
    gioiTinh_string1 = gioiTinh_mapping1.get(phieu['gioi_tinh'], 'Unknown')
    gioiTinh_boolean1 = 'Nam' if gioiTinh_string1 == 0 else 'Nữ'
    b = BenhNhan(ho=phieu['ho'], ten=phieu['ten'],\
                 ngay_sinh=phieu['ngay_sinh'], gioi_tinh= 0 if gioiTinh_boolean1 == 'Nam' else 1, diachi=phieu['diachi'],\
                email=phieu['email'],so_dien_thoai=phieu['so_dien_thoai'])
    db.session.add(b)
    db.session.commit()


if __name__ == '__main__':
    with app.app_context():
        print(receipt_detail_info(2024, 2))
