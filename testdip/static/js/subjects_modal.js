console.log("JavaScript файл загружен и выполняется");

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM полностью загружен и обработан");

    const saveChangesBtn = document.getElementById("save-changes");

    saveChangesBtn.addEventListener("click", function () {
        // Получаем все select элементы с классом subject-select и cabinet-select
        const subjectSelects = document.querySelectorAll('.subject-select');
        const cabinetSelects = document.querySelectorAll('.cabinet-select');

        // Создаем массив объектов с данными для каждой пары
        const scheduleData = [];

        subjectSelects.forEach((subjectSelect, index) => {
            const pairId = subjectSelect.dataset.pairId;
            const subjectId = subjectSelect.value;
            const cabinetId = cabinetSelects[index].value; // Получаем cabinetId из соответствующего cabinetSelect

            scheduleData.push({
                pairId: pairId,
                subjectId: subjectId,
                cabinetId: cabinetId
            });
        });

        // Отправляем данные на сервер
        fetch('/schedule/save_changes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(scheduleData)
        })
        .then(response => {
            if (response.ok) {
                alert('Изменения сохранены');
                location.reload(); // Перезагружаем страницу для отображения изменений
            } else {
                alert('Ошибка при сохранении изменений');
            }
        });
    });

    // Добавляем обработчики для изменения кабинета и предмета
    document.querySelectorAll('.cabinet-select').forEach(select => {
        select.addEventListener('change', function () {
            saveChange(this, 'cabinet');
            checkConflicts();
        });
    });

    document.querySelectorAll('.subject-select').forEach(select => {
        select.addEventListener('change', function () {
            saveChange(this, 'subject');
            checkConflicts();
        });
    });

    function saveChange(selectElement, type) {
        const pairId = selectElement.dataset.pairId;
        const value = selectElement.value;
        const url = type === 'cabinet' ? `/schedule/update_cabinet/${pairId}/` : `/schedule/update_subject/${pairId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ value: value })
        }).then(response => {
            if (!response.ok) {
                alert('Ошибка при сохранении изменений');
            }
        });
    }

    function checkConflicts() {
        const rows = document.querySelectorAll('tr');
        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const cabinets = {};
            const subjects = {};

            cells.forEach(cell => {
                const cabinet = cell.querySelector('.cabinet-select')?.value;
                const subject = cell.querySelector('.subject-select')?.value;

                if (cabinet) {
                    if (cabinets[cabinet]) {
                        cell.style.backgroundColor = 'red';
                        cabinets[cabinet].style.backgroundColor = 'red';
                    } else {
                        cabinets[cabinet] = cell;
                    }
                }

                if (subject) {
                    if (subjects[subject]) {
                        cell.style.backgroundColor = 'red';
                        subjects[subject].style.backgroundColor = 'red';
                    } else {
                        subjects[subject] = cell;
                    }
                }
            });
        });
    }

    // Обработчики для удаления и изменения очередности пар
    document.querySelectorAll('.delete-pair').forEach(button => {
        button.addEventListener('click', function () {
            const pairId = this.dataset.pairId;
            fetch(`/schedule/delete/${pairId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                }
            });
        });
    });

    document.querySelectorAll('.move-up').forEach(button => {
        button.addEventListener('click', function () {
            const pairId = this.dataset.pairId;
            fetch(`/schedule/move_up/${pairId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                }
            });
        });
    });

    document.querySelectorAll('.move-down').forEach(button => {
        button.addEventListener('click', function () {
            const pairId = this.dataset.pairId;
            fetch(`/schedule/move_down/${pairId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            }).then(response => {
                if (response.ok) {
                    location.reload();
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});