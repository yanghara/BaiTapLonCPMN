function tinhTongTien() {
	let a = parseFloat(document.getElementById("tienKham").value);
    let b = parseFloat(document.getElementById("tienThuoc").value);
    let sum = a + b;
    document.getElementById('tongTien').innerText = sum.toFixed(0);
    }

window.onload = function() {
    var myBtnTinhTong = document.getElementById('btnTinhTong');

    myBtnTinhTong.addEventListener('onclick', tinhTongTien);
}