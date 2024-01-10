from app import db, app
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import enum
from datetime import datetime



class UserRoleEnum(enum.Enum):
    BenhNhan = 1
    BacSi = 2
    YTa = 3
    Admin = 4
    ThuNgan = 5


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())


class User(BaseModel, UserMixin):
    __tablename__ = 'User'

    name = Column(String(50), nullable=False, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(150), nullable=False)
    avatar = Column(String(150),
                    default='https://res.cloudinary.com/drv8vy8ww/image/upload/v1703861612/m2i3dxfctpt5dmmhxstd.png')
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.BenhNhan)

    bac_si = relationship('BacSi', backref="user", lazy=True, uselist=False)
    thu_ngan = relationship('ThuNgan', backref="user", lazy=True, uselist=False)
    y_ta = relationship('YTa', backref="user", lazy=True, uselist=False)
    benh_nhan = relationship('BenhNhan', backref="user", lazy=True)
    admin = relationship('Admin', backref="user", lazy=True, uselist=False)

    def __str__(self):
        return self.name


class BacSi(db.Model):
    __tablename__ = 'BacSi'

    id = Column(Integer,ForeignKey(User.id), primary_key=True)
    ho_ten = Column(String(150), nullable=False)
    chuyen_mon = Column(String(150))
    bang_cap = Column(String(150))

    phieu_kham_benh = relationship('PhieuKhamBenh', backref="bacsi", lazy=True)


class ThuNgan(db.Model):
    __tablename__ = 'ThuNgan'

    id = Column(Integer,ForeignKey(User.id), primary_key=True)
    ho_ten = Column(String(150), nullable=False)
    trinh_do = Column(String(150))

    hoa_don = relationship('HoaDon', backref="thungan", lazy=True)


class YTa(db.Model):
    __tablename__ = 'YTa'

    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    ho_ten = Column(String(150), nullable=False)
    ca_lam = Column(Integer, nullable=False)
    danh_sach_kham = relationship('DanhSachKham', backref="yta", lazy=True)


class Admin(db.Model):
    __tablename__ = 'Admin'

    id = Column(Integer, ForeignKey(User.id), primary_key=True)
    ho_ten = Column(String(150), nullable=False)
    chuc_vu = Column(String(150), nullable=False)

    bao_cao = relationship('BaoCaoThongKe', backref="admin", lazy=True)


class BaoCaoThongKe(BaseModel):
    __tablename__ = 'BaoCaoThongKe'

    id = Column(Integer, primary_key=True, nullable=False)
    thang = Column(Integer, nullable=False)

    admin_id = Column(Integer, ForeignKey(Admin.id))


class HoaDon(BaseModel):
    __tablename__ = 'HoaDon'

    id = Column(Integer, autoincrement=True , primary_key=True, nullable=False)
    receipt_details = relationship('ReceiptDetails', backref='hoadon', lazy=True)

    thu_ngan_id = Column(Integer, ForeignKey(ThuNgan.id))
    phieu_kham_benh = relationship('PhieuKhamBenh', backref="hoadon", lazy=True, uselist=False)
    benh_nhan = relationship('BenhNhan', backref="hoadon", lazy=True, uselist=False)


class DonViThuoc(db.Model):
    __tablename__ = 'DonViThuoc'

    id = Column(Integer, primary_key=True)
    ten = Column(String(100), nullable=False)

    thuoc = relationship('Thuoc', backref='donvithuoc', lazy=True)


class Thuoc(db.Model):
    __tablename__ = 'Thuoc'

    id = Column(String(5), primary_key=True)
    name = Column(String(150), nullable=False, unique=True)
    ngaysanxuat = Column(DateTime)
    hansudung = Column(DateTime, default=datetime.now())
    dongia = Column(Float, nullable=False, unique=True)

    don_vi_thuoc_id = Column(Integer, ForeignKey(DonViThuoc.id), nullable=False)

    chi_tiet_toa_thuoc = relationship('ChiTietToaThuoc', backref='Thuoc', lazy=True)


class DanhSachKham(db.Model):
    __tablename__ = 'DanhSachKham'
    id = Column(String(10), primary_key=True)
    ngay_kham = Column(DateTime, default=datetime.now())
    so_benh_nhan = Column(Integer, default=40)

    y_ta_id = Column(Integer, ForeignKey(YTa.id))
    benh_nhan = relationship('BenhNhan', backref="danhsachkham", lazy=True)


class BenhNhan(db.Model):
    __tablename__ = 'BenhNhan'

    id = Column(Integer,ForeignKey(User.id), primary_key=True, autoincrement=True)
    ho = Column(String(150), nullable=False)
    ten = Column(String(150), nullable=False)
    ngay_sinh = Column(DateTime)
    gioi_tinh = Column(Boolean, default=0)
    diachi = Column(String(150), unique=True)
    email = Column(String(150), unique=True)
    so_dien_thoai = Column(Integer)

    danh_sach_kham_id = Column(String(10), ForeignKey(DanhSachKham.id))
    hoa_donid = Column(Integer, ForeignKey(HoaDon.id))
    phieu_kham = relationship('PhieuKhamBenh', backref="benhnhan", lazy=True)


class PhieuKhamBenh(db.Model):
    __tablename__ = 'PhieuKhamBenh'

    id = Column(Integer, primary_key=True, autoincrement=True)
    ngay_kham = Column(DateTime, default=datetime.now())
    trieu_chung = Column(String(100), nullable=False)
    du_doan_benh = Column(String(100), nullable=False)

    benh_nhan_id = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    bac_si_id = Column(Integer, ForeignKey(BacSi.id), nullable=False)
    hoa_don = Column(Integer, ForeignKey(HoaDon.id))

    chi_tiet_toa_thuoc = relationship('ChiTietToaThuoc', backref='PhieuKhamBenh', lazy=True)


class ChiTietToaThuoc(BaseModel):
    so_luong = Column(Integer, nullable=False)
    lieu_luong = Column(String(150), nullable=False)
    cach_dung = Column(String(150), nullable=False)
    phieu_kham_id = Column(Integer, ForeignKey(PhieuKhamBenh.id), nullable=False)
    thuoc_id = Column(String(5), ForeignKey(Thuoc.id))


class ReceiptDetails(BaseModel):
    benhNhanId = Column(Integer, ForeignKey(BenhNhan.id), nullable=False)
    receiptId = Column(Integer, ForeignKey(HoaDon.id), nullable=False)
    ho = Column(String(50), default=0)
    ten = Column(String(100), default=0)
    ngaySinh = Column(DateTime,default=0)
    gioiTinh = Column(Boolean,default=0) #0 - nam; 1 - nu
    diaChi = Column(String(100),default=0)

    ngayKham = Column(DateTime, nullable=False)
    tienKham = Column(Float, default=100000)
    tienThuoc = Column(Float, default=0)
    tongTien = Column(Float, default=0)



if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()

        import hashlib

        u1 = User(name='Van', username='hara', password=str(hashlib.md5('abcabc'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.BenhNhan)
        u2 = User(name='NhatThao', username='thaovu', password=str(hashlib.md5('18062003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.BacSi)
        u3 = User(name='ThanhThuy', username='thuythuhai', password=str(hashlib.md5('24112003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.Admin)
        u4 = User(name='vanvan', username= 'vanvan', password=str(hashlib.md5('26112003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.YTa)
        u5 = User(name='hara', username='vavan', password=str(hashlib.md5('26112003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.YTa)
        u6 = User(name='Thuy', username='thuy', password=str(hashlib.md5('2003'.encode('utf-8')).hexdigest()),
                  user_role=UserRoleEnum.ThuNgan)
        yta1 = YTa(id=4,ho_ten='Trần Thị B', ca_lam=9)
        dsk1 = DanhSachKham(id= "DS01",so_benh_nhan=10, y_ta_id=4)
        dvT1 = DonViThuoc(ten='Viên')
        dvT2 = DonViThuoc(ten='Vỉ')
        dvT3 = DonViThuoc(ten='Chai')
        thuoc1 = Thuoc(id='T01',name='Paracetamol', ngaysanxuat='2021-12-12',dongia='20000', don_vi_thuoc_id = 1)
        thuoc2 = Thuoc(id='T02',name='Penicilin', ngaysanxuat='2023-01-02', dongia='10000', don_vi_thuoc_id=2)
        thuoc3 = Thuoc(id='T03',name='Mometasone', ngaysanxuat='2023-02-11',hansudung='2024-04-04',dongia='12000', don_vi_thuoc_id=3)
        bn1 = BenhNhan(id=1, ho='Nguyen Van',ten='C',ngay_sinh="2003-12-04", gioi_tinh=0,
                       diachi='huynh tan phat, nha be', email='yanghara@gmail.com',
                       so_dien_thoai='0123762475', danh_sach_kham_id = "DS01")
        bn2 = BenhNhan(id=2, ho='Nguyễn Thị', ten='Cúc', ngay_sinh="2003-06-12", gioi_tinh=0,
                       diachi='Nhơn Đức, Nhà Bè', email='yan@gmail.com',
                       so_dien_thoai='0123764475', danh_sach_kham_id="DS01")

        bs1 = BacSi(id=1, chuyen_mon='Tai, Mũi, Họng',bang_cap='Gioi', ho_ten='Nguyen Trong N')
        pk1 = PhieuKhamBenh(id=1, ngay_kham='2023-01-5', trieu_chung='Viêm họng, Ho, Sỗ mũi', du_doan_benh='Cảm', benh_nhan_id=1, bac_si_id=1)
        toathuoc1 = ChiTietToaThuoc(thuoc_id='T01', phieu_kham_id=1, so_luong=5, lieu_luong='2 viên/ngày', cach_dung='Uống sau khi ăn', created_date='2023-01-5')
        bs2 = BacSi(id=2, chuyen_mon='Hệ Tiêu Hóa', bang_cap='Khá', ho_ten='Nguyễn Bài Tập')
        toathuoc2 = ChiTietToaThuoc(thuoc_id='T03',phieu_kham_id=2, so_luong=2, lieu_luong='1 viên/ngày', cach_dung='Uống trước khi ăn', created_date='2023-11-15')
        pk2 = PhieuKhamBenh(id=2, ngay_kham='2023-11-15', trieu_chung='Đau bụng, biếng ăn', du_doan_benh='Đau dạ dày',
                            benh_nhan_id=2, bac_si_id=2)
        bn3 = BenhNhan(id=3, ho='Nguyễn Ngọc', ten='Thu', ngay_sinh="2003-12-2", gioi_tinh=0,
                                      diachi='Võ Văn Tần,Quận 3', email='ngocthu@gmail.com',
                                      so_dien_thoai='0134964475', danh_sach_kham_id="DS01")


        db.session.add_all([u1,u2,u3,u4,u5,u6,yta1,dsk1,thuoc1,
                            thuoc2,thuoc3,bn1,bn2,bn3,bs1,bs2,pk1,pk2,toathuoc2,toathuoc1,dvT1,dvT2,dvT3])
        db.session.commit()
