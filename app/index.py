from flask import render_template, request, redirect, session, jsonify
import dao
from app.Models import User, BenhNhan, YTa, BacSi, ThuNgan, UserRoleEnum
from app import app, login, utils
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
def index():
    cate = ""
    if not current_user.is_authenticated:
        return render_template('index.html')
    else:
        if current_user.user_role == UserRoleEnum.BenhNhan:
            cate = dao.load_benh_nhan()
        elif current_user.user_role == UserRoleEnum.BacSi:
            cate = dao.load_bac_si()
        elif current_user.user_role == UserRoleEnum.YTa:
            cate = dao.load_y_ta()
        elif current_user.user_role == UserRoleEnum.ThuNgan:
            cate = dao.load_benh_nhan()

        return render_template('index.html', header=cate, types=current_user.user_role.name)


@app.route('/login', methods=['get', 'post'])
def process_login_user():
    err_msg = None
    if request.method.__eq__('POST'):
        types = request.form.get('selectuser')
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password, type=types)
        if types == UserRoleEnum.BenhNhan.name:
            if user:
                login_user(user=user)

                return redirect('/BenhNhan')
            else:
                err_msg = "Tài khoản đăng nhập không chính xác"
        elif types == UserRoleEnum.BacSi.name:
            if user:
                login_user(user=user)

                return redirect('/BacSi')
            else:
                err_msg = "Tài khoản đăng nhập không chính xác"
        elif types == UserRoleEnum.YTa.name:
            if user:
                login_user(user=user)

                return redirect('/YTa')
            else:
                err_msg = "Tài khoản đăng nhập không chính xác"
        elif types == UserRoleEnum.ThuNgan.name:
            if user:
                login_user(user=user)

                return redirect('/ThuNgan')
            else:
                err_msg = "Tài khoản đăng nhập không chính xác"
        else:
            if user:
                login_user(user=user)

                return redirect('/admin')
            else:
                err_msg = "Tài khoản đăng nhập không chính xác"
    return render_template('login.html', err_msg=err_msg)


@app.route('/YTa', methods=['get'])
@login_required
def test_user_role_nurse():
    if current_user.user_role == UserRoleEnum.YTa:
        cates = dao.load_y_ta()

        return render_template('/index.html', header=cates, types=current_user.user_role.name)


@app.route('/YTa/1')
def dang_ky_truc_tiep():
    if current_user.user_role == UserRoleEnum.YTa:
        cates = dao.load_y_ta()

    return render_template('yta/dangkyoff.html', header=cates)


@app.route('/YTa/2')
def danh_sach_kham():
    if current_user.user_role == UserRoleEnum.YTa:
        cates = dao.load_y_ta()

    PatientDetail = dao.load_patient()

    return render_template('yta/danhsachkham.html', header=cates , PatientDetail=PatientDetail)



@app.route("/api/info_patient", methods=['post'])
def register_offline():
    data = request.json

    patient = session.get('patient')

    if patient is None:
        patient = {}

    if not data.get("ho") or not data.get("ten") \
            or not data.get("diachi") or not str(data.get("ngay_sinh")) \
            or not data.get("diachi") or not str(data.get("ngayDangKy")) or not data.get("so_dien_thoai"):
        pass
    else:
        patient = {
            "ho": data.get("ho"),
            "ten": data.get("ten"),
            "ngay_sinh": str(data.get("ngay_sinh")),
            "gioi_tinh": str(data.get("gioi_tinh")),
            "diachi": data.get("diachi"),
            "ngayDangKy": str(data.get("ngayDangKy")),
            "so_dien_thoai": data.get("so_dien_thoai")

        }
        print(patient)
        dao.add_patient(patient)

        session['patient'] = patient  # luu vao session1
    return patient


@app.route('/ThuNgan', methods=['get'])
@login_required
def test_user_role_cashier():
    if current_user.user_role == UserRoleEnum.ThuNgan:
        cates = dao.load_thu_ngan()

        return render_template('/index.html', header=cates, types=current_user.user_role.name)


@app.route('/ThuNgan/1')
def thanh_toan_hoa_don():
    if current_user.user_role == UserRoleEnum.ThuNgan:
        cates = dao.load_thu_ngan()

    return render_template('thungan/thanhtoanhoadon.html', header=cates)


@app.route("/api/info_receipt", methods=['post'])
def add_to_receipt():
    '''
        #cấu trúc của 1 hóa đơn
        #dat 1 cai key tên là 'receipt'
        "receipt" : {
        "1":{ #mã số 1 là key -> lưu thông tin
            "benhNhanId":"1",
            "ho":"Nguyen",
            "ten" = "Van C",
            "ngaySinh" = 1/1/2002,
            "gioiTinh" = 0,
            "diaChi" = "7 ABC, quan 8, TPHCM",

            "ngayKham" = 1/1/2022,
            "tienKham" = 100000,
            "tienThuoc" = 25000,
            "tongTien" = 125000
            }
        }
    :return:
    '''
    data = request.json

    # tao hoa don
    receipt = session.get('receipt')

    # kiem tra da co du lieu trong hoa don chua -> neu chua thi tao
    if receipt is None:
        receipt = {}

    # kiem tra da tao hoa don cho ma benh nhan chua
    id = str(data.get("benhNhanId"))
    if id not in receipt:  # nếu mã bệnh nhân chưa được tạo hóa đơn
        # đưa thông tin bệnh nhân vào biến receipt - lưu kiểu từ điển
        # if not data.get("benhNhanId") or not data.get("ho") or not data.get("ten")\
        #     or not data.get("diaChi") or not str(data.get("ngaySinh")) or not str(data.get("ngayKham")) or not float(data.get("tienThuoc")):
        #     pass
        # else:
        receipt[id] = {
            "benhNhanId": data.get("benhNhanId"),  # lấy từ data gửi lên
            "ho": data.get("ho"),
            "ten": data.get("ten"),
            "ngaySinh": str(data.get("ngaySinh")),
            "gioiTinh": str(data.get("gioiTinh")),
            "diaChi": data.get("diaChi"),
            "ngayKham": str(data.get("ngayKham")),
            "tienKham": data.get("tienKham"),
            "tienThuoc": float(data.get("tienThuoc")),
            "tongTien": data.get("tongTien")
        }
        print(receipt[id])
        dao.add_receipt(receipt)
        del receipt[id]
        session['receipt'] = receipt  # luu vao session1

    # else:  # nếu mã bệnh nhân đã được tạo hóa đơn
    #     print("Bệnh nhân đã có hóa đơn.")

    return jsonify(utils.count_receipt(receipt))


@app.route('/BenhNhan', methods=['get'])
@login_required
def test_user_role_patient():
    if current_user.user_role == UserRoleEnum.BenhNhan:
        cates = dao.load_benh_nhan()

        return render_template('/index.html', header=cates, types=current_user.user_role.name)


@app.route('/BenhNhan/1')
@login_required
def dang_ky_lich_kham():
    global cates
    if current_user.user_role == UserRoleEnum.BenhNhan:
        cates = dao.load_benh_nhan()

    return render_template('/BenhNhan/dkylichkham.html', header=cates)


@app.route("/api/info_patient_onl", methods=['post'])
def register_online():
    data = request.json

    nguoibenh = session.get('nguoibenh')

    if nguoibenh is None:
        nguoibenh = {}

    nguoibenh = {
        "ho": data.get("ho"),
        "ten": data.get("ten"),
        "ngay_sinh": str(data.get("ngay_sinh")),
        "gioi_tinh": str(data.get("gioi_tinh")),
        "diachi": data.get("diachi"),
        "email": data.get("email"),
        "ngayKham": str(data.get("ngayKham")),
        "so_dien_thoai": data.get("so_dien_thoai")

    }
    print(nguoibenh)
    dao.add_patient_onl(nguoibenh)

    session['nguoibenh'] = nguoibenh  # luu vao session1
    return nguoibenh

@app.route('/BacSi', methods=['get'])
@login_required
def test_user_role_doctor():
    global cates
    if current_user.user_role == UserRoleEnum.BacSi:
        cates = dao.load_bac_si()
    return render_template('/index.html', header=cates, types=current_user.user_role.name)


@app.route('/BacSi/2', methods=['get', 'post'])
def ke_toa_thuoc():
    global cates
    if current_user.user_role == UserRoleEnum.BacSi:
        cates = dao.load_bac_si()
    return render_template('BacSi/ketoathuoc.html', header=cates)


@app.route('/lichsubenh', methods=['get', 'post'])
def xem_lich_su_benh():
    global cates, benhnhan2, tt
    if current_user.user_role == UserRoleEnum.BacSi:
        cates = dao.load_bac_si()

    mabn = request.form.get('idpatient')
    tt = dao.get_benh_nhan_by_id(mabn)
    benhnhan2 = dao.get_lich_su_benh(mabn)

    if benhnhan2 in benhnhan2:
        del benhnhan2

    if tt in tt:
        del tt
    return render_template('BacSi/lichsubenh.html',
                           header=cates, patient=tt, lichsubenh=benhnhan2)


@app.route('/tracuuthuoc', methods=['get', 'post'])
def xem_tra_cuu_thuoc():
    if current_user.user_role == UserRoleEnum.BacSi:
        cates = dao.load_bac_si()
    kw = request.args.get("keywordthuoc")

    drugs = dao.load_medicine2(kw=kw)
    return render_template('BacSi/tracuuthuoc2.html', header=cates, drugs=drugs)


@app.route('/BacSi/1', methods=['get', 'post'])
@login_required
def create_examination_form():
    if current_user.user_role == UserRoleEnum.BacSi:
        cates = dao.load_bac_si()

    thuoc = dao.load_medicine()
    if request.method.__eq__('POST'):
        benh_nhan_id = request.form.get('id')
        name = request.form.get('name')
        date = request.form.get('date')
        symptom = request.form.get('symptom')
        disease = request.form.get('disease')
        medicineName = request.form.get('medicineName')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit')
        instruction = request.form.get('instruction')

        dao.add_examination_form(benh_nhan_id=benh_nhan_id,
                                 name=name,
                                 date=date,
                                 symptom=symptom,
                                 disease=disease,
                                 medicineName=medicineName,
                                 quantity=quantity,
                                 unit=unit,
                                 instruction=instruction,
                                 id=current_user.id)

    return render_template('BacSi/lapphieukham.html', thuoc=thuoc, header=cates)


@app.route('/api/tracuuthuoc', methods=['post'])
def add_thuoc():
    data = request.json

    medicine = session.get('medicine')

    if medicine is None:
        medicine = {}

    id = str(data.get('id'))
    if id in medicine:
        medicine[id]['quantity'] += 1
    else:
        medicine[id] = {
            "id": id,
            "name": data.get("name"),
            "donvi": data.get("donvi"),
            "quantity": 1
        }

    session['medicine'] = medicine

    return jsonify(utils.count_thuoc(medicine))


@app.route('/api/tracuuthuoc/<thuoc_id>', methods=['delete'])
def delete_cart(thuoc_id):
    medicine = session.get('medicine')
    if medicine and thuoc_id in medicine:
        del medicine[thuoc_id]

    session['medicine'] = medicine

    return jsonify(utils.count_thuoc(medicine))


@login.user_loader  # mỗi lần login xong tự động nó sẽ get đối tượng user từ db và nó gắn cho cái biến current
def get_user(user_id):
    return dao.get_user_by_id(user_id)


@app.route('/register', methods=['get', 'post'])
def register_user():
    err_msg = None

    if request.method.__eq__('POST'):
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if password.__eq__(confirm):
            try:
                dao.add_user(name=request.form.get('name'),
                             username=request.form.get('username'),
                             password=password,
                             avatar=request.files.get('avatar'),
                             user_role=request.form.get('selectuser'))
            except Exception as ex:
                print(str(ex))
                err_msg = 'Hệ thống đang bị lỗi'
            else:
                return redirect('/login')
        else:
            err_msg = 'Mật khẩu KHÔNG khớp!!!'

    return render_template('/register.html', err_msg=err_msg)


@app.route('/logout')
def process_logout():
    logout_user()
    return redirect('/login')


@app.route('/contact')
def process_contact():
    cate = ""
    if not current_user.is_authenticated:
        return render_template('index.html')
    else:
        if current_user.user_role == UserRoleEnum.BenhNhan:
            cate = dao.load_benh_nhan()
        elif current_user.user_role == UserRoleEnum.BacSi:
            cate = dao.load_bac_si()
        elif current_user.user_role == UserRoleEnum.YTa:
            cate = dao.load_y_ta()
        elif current_user.user_role == UserRoleEnum.ThuNgan:
            cate = dao.load_benh_nhan()

    return render_template('/contact.html', header=cate)


@app.route('/admin/login', methods=['post', 'get'])
def login_admin():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.auth_user(username=username,
                             password=password,
                             type=UserRoleEnum.Admin.name)

        if user:
            login_user(user=user)

    return redirect('/admin')


if __name__ == '__main__':
    from app import admin

    app.run(debug=True)
