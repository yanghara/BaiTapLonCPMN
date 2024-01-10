function dangKyKhamAPI(ngayDangKy, ho, ten, ngay_sinh, gioi_tinh, diachi, so_dien_thoai){
    fetch("/api/info_patient", {
        method: "post",
        body: JSON.stringify({
            "ho": ho,
            "ten": ten,
            "ngay_sinh": ngay_sinh,
            "gioi_tinh": gioi_tinh,
            "diachi": diachi,
            "ngayDangKy": ngayDangKy,
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
function dangKyKham() {
    let ho1 = document.getElementById('ho').value;
    let ten1 = document.getElementById('ten').value;
    let ngaySinh1 = document.getElementById('ngaySinh').value;

    var selectedGender = document.querySelector('input[name="flexRadioDefault"]:checked');

    let gioiTinh1 = selectedGender.value;
    let diaChi1 = document.getElementById('diaChi').value;
     let ngayDangKy1 = document.getElementById('ngayDangKy').value;
    let soDienThoai1 = document.getElementById('soDienThoai').value;

    dangKyKhamAPI(ngayDangKy1, ho1, ten1, ngaySinh1, gioiTinh1, diaChi1, soDienThoai1)
}


window.onload = function() {
    var myBtnDangKy = document.getElementById('btnDangKy');
    myBtnDangKy.addEventListener('onclick', dangKyKham);
}