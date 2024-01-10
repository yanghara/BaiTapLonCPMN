function luuHoaDonAPI(benhNhanId, ho, ten, ngaySinh, gioiTinh, diaChi, ngayKham, tienKham, tienThuoc, tongTien){
        fetch("/api/info_receipt", {
        method: "post",
        body: JSON.stringify({
              "benhNhanId": benhNhanId,
                "ho": ho,
                "ten": ten,
                "ngaySinh": ngaySinh,
                "gioiTinh": gioiTinh,
                "diaChi": diaChi,
                "ngayKham": ngayKham,
                "tienKham": tienKham,
                "tienThuoc": tienThuoc,
                "tongTien": tongTien
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res){
        return res.json();
    }).then(function(data){
       console.info(data)
          if (!benhNhanId || !ho || !ten || !diaChi || !ngaySinh || !ngayKham || !tienThuoc) {
            alert('Vui lòng điền đầy đủ thông tin bắt buộc.');
            return false; // Prevent form submission
          }
       alert('Hóa đơn tạo thành công')
//            for i in info:
//                if (benhNhanId==i.id and ho==i.ho and ten==i.ten and diaChi==i.diachi and ngaySinh==i.ngaysinh and gioiTinh==i.gioitinh)
//                    {
//
//                    return true
//                    }
//            alert('Thong tin benh nhan khong khop!')

    });
}

function luuHoaDon() {
    let benhNhanId1 = document.getElementById('benhNhanId').value;
    let ho1 = document.getElementById('ho').value;
    let ten1 = document.getElementById('ten').value;
    let ngaySinh1 = document.getElementById('ngaySinh').value;

    var selectedGender = document.querySelector('input[name="flexRadioDefault"]:checked');

    let gioiTinh1 = selectedGender.value;
    let diaChi1 = document.getElementById('diaChi').value;
     let ngayKham1 = document.getElementById('ngayKham').value;
    let tienKham1 = document.getElementById('tienKham').value;
    let tienThuoc1 = document.getElementById('tienThuoc').value;
    let tongTien1 = document.getElementById('tongTien').innerText;

    luuHoaDonAPI(benhNhanId1, ho1, ten1, ngaySinh1, gioiTinh1, diaChi1, ngayKham1, tienKham1, tienThuoc1, tongTien1)
}

window.onload = function() {
    var myBtnLuuHD = document.getElementById('btnLuuHD');
    myBtnLuuHD.addEventListener('onclick', luuHoaDon);
}