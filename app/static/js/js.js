function addToMedicine(id, name, donvi){
    fetch('/api/tracuuthuoc', {
        method: 'post',
        body: JSON.stringify({
            "id": id,
            "name": name,
            "donvi": donvi
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(function(res) {
        return res.json();
    }).then(function(data) {
        console.info(data)
//        let items = document.getElementsByClassName("cart-counter");
//        for (let item of items)
//            item.innerText = data.total_quantity
    }).catch(function (err){
        console.error(err)
    });
}

function deleteMedicine(id, obj) {
    obj.disbaled = true;
    if (confirm("Bạn Chắc Chắn Xóa Thuốc Này Không?") === true) {
        fetch(`/api/tracuuthuoc/${id}`, {
            method: 'delete'
        }).then(function(res) {
            return res.json();
        }).then(function(data) {
            obj.disabled = false;
            let d = document.getElementById(`thuoc${id}`);
            d.style.display = "none";
        });
    }
}

function saveDataExams() {
    let benhnhanid = document.getElementById('id').value;
    let name = document.getElementById('name').value;
    let symptom = document.getElementById('symptom').value;
    let disease = document.getElementById('disease').value;
    let medicineName = document.getElementById('medicineName').value;
    let quantity = document.getElementById('quantity').value;
    let unit = document.getElementById('unit').value;
    let instruction = document.getElementById('instruction').value;

    let examData = {
        'id': benhnhan_id,
        'name': name,
        'date': date,
        'symptom': symptom,
        'disease': disease,
        'medicineName': medicineName,
        'quantity': quantity,
        'unit': unit,
        'instruction': instruction
    };

    fetch('/api/save_exam_data', {
        method: 'post',
        body: JSON.stringify(examData),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => {
        console.info(res)
        return res.json()
    }).then(data => {
        console.info(data)
    }).catch(err => {
        console.error(err)
    })
};


