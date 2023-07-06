function addRow() {
    var template = document.getElementById('new-row-template');
    var table = document.getElementById("tableReports");
    var newRow = template.cloneNode(true);
    newRow.removeAttribute('id');
    newRow.style.display = '';
    table.appendChild(newRow);
}

const deleteIcons = document.querySelectorAll('.delete-icon');
const deleteIconsInvests = document.querySelectorAll('.delete-icon-invest');

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

// Обойти каждый элемент и назначить обработчик клика
deleteIconsInvests.forEach(deleteIconsInvest => {
    deleteIconsInvest.addEventListener('click', function() {
        const row = this.parentNode; // Получить родительскую строку
        const code = this.getAttribute('data-code');

        // Получить CSRF-токен из cookies
        const csrftoken = getCookie('csrftoken');

        // Выполнить AJAX-запрос для удаления строки с использованием кода `code`
        fetch(`/reports/delete-investi/${code}/`, {
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

// Цикл для обработки каждого поля
for (let i = 1; i <= 7; i++) {
    const inputDate = document.getElementById(`data_${i}`);
    
    if (inputDate) {
      inputDate.addEventListener('keydown', event => {
        const key = event.key;
        if (!/\d/.test(key) && key !== 'Backspace' && key !== 'Delete' && key !== 'ArrowLeft' && key !== 'ArrowRight') {
          event.preventDefault();
        }
      });
    
      inputDate.addEventListener('input', () => {
        let dateValue = inputDate.value.replace(/[^\d]/g, ''); // Удаляем все символы, кроме цифр
        if (dateValue.length === 8) { // Проверяем, что введено 8 цифр (ддммгггг)
          const day = dateValue.slice(0, 2);
          const month = dateValue.slice(2, 4);
          const year = dateValue.slice(4, 8);
    
          const formattedDate = `${day}.${month}.${year}`;
          inputDate.value = formattedDate;
        }
      });
    }
  }