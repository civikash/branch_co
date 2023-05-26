function addRow() {
    var template = document.getElementById('new-row-template');
    var table = document.getElementById("tableReports");
    var newRow = template.cloneNode(true);
    newRow.removeAttribute('id');
    newRow.style.display = '';
    table.appendChild(newRow);
}

const deleteIcons = document.querySelectorAll('.delete-icon');

// Обойти каждый элемент и назначить обработчик клика
deleteIcons.forEach(deleteIcon => {
    deleteIcon.addEventListener('click', function() {
        const row = this.parentNode; // Получить родительскую строку
        const code = this.getAttribute('data-code');

        // Получить CSRF-токен из cookies
        const csrftoken = getCookie('csrftoken');

        // Выполнить AJAX-запрос для удаления строки с использованием кода `code`
        fetch(`/reports/delete-marfa/${code}/`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // После успешного удаления строки из базы данных, удалить саму строку из таблицы:
                row.remove();
            } else {
                console.error(data.message);
            }
        })
        .catch(error => {
            console.error('Ошибка при выполнении AJAX-запроса:', error);
        });
    });
});

// Функция для получения значения cookie по имени
function getCookie(name) {
    const cookieValue = document.cookie.match('(^|;)\\s*' + name + '=([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}