function dangKyKhamOnlAPI(ngayKham, ho, ten, ngay_sinh, gioi_tinh, diachi, email, so_dien_thoai){
    fetch("/api/info_patient_onl", {
        method: "post",
        body: JSON.stringify({
            "ho": ho,
            "ten": ten,
            "ngay_sinh": ngay_sinh,
            "gioi_tinh": gioi_tinh,
            "diachi": diachi,
            "email": email,
            "ngayKham": ngayKham,
            "so_dien_thoai": so_dien_thoai
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        return res.json();
    }).then(function(data){
        console.info(data)
          if (!ho || !ten || !diachi || !ngay_sinh || !so_dien_thoai) {
            alert('Vui lòng điền đầy đủ thông tin bắt buộc.');
            return false;
        }
        //return true;
        alert('Đăng ký khám thành công!');

    });
}
//body là dữ liệu đóng gói vào trong thân của http request gửi lên
//header đối tượng json -> promise
function dangKyKhamOnl() {
    let ho1 = document.getElementById('ho').value;
    let ten1 = document.getElementById('ten').value;
    let ngaySinh1 = document.getElementById('ngaySinh').value;

    var selectedGender = document.querySelector('input[name="gioiTinh"]:checked');

    let gioiTinh1 = selectedGender.value;
    let diaChi1 = document.getElementById('diaChi').value;
    let email1 = document.getElementById('eMail').value;
     let ngayKham1 = document.getElementById('ngayKham').value;
    let soDienThoai1 = document.getElementById('soDienThoai').value;

    dangKyKhamOnlAPI(ngayKham1, ho1, ten1, ngaySinh1, gioiTinh1, diaChi1, email1, soDienThoai1)
}


window.onload = function() {
    var myBtnDangKy = document.getElementById('btnDangKyOnl');
    myBtnDangKy.addEventListener('onclick', dangKyKhamOnl);
}