window.addEventListener('load', function () {
  var column1Sum = 0;
  var column2Sum = 0;
  var column3Sum = 0;

  var column1Inputs = document.querySelectorAll('input[name^="cladiri_"]');
  var column2Inputs = document.querySelectorAll('input[name^="apart_"]');
  var column3Inputs = document.querySelectorAll('input[name^="sup_total_"]');

  updateSums();

  function updateSums() {
    column1Sum = 0;
    column2Sum = 0;
    column3Sum = 0;

    for (var i = 0; i < column1Inputs.length; i++) {
      var value = parseFloat(column1Inputs[i].value);
      if (!isNaN(value)) {
        column1Sum += value;
      }
    }

    for (var i = 0; i < column2Inputs.length; i++) {
      var value = parseFloat(column2Inputs[i].value);
      if (!isNaN(value)) {
        column2Sum += value;
      }
    }

    for (var i = 0; i < column3Inputs.length; i++) {
      var value = parseFloat(column3Inputs[i].value);
      if (!isNaN(value)) {
        column3Sum += value;
      }
    }

    var newColumn1Inputs = document.querySelectorAll('input[name^="new_cladiri_"]');
    var newColumn2Inputs = document.querySelectorAll('input[name^="new_apart_"]');
    var newColumn3Inputs = document.querySelectorAll('input[name^="new_sup_total_"]');

    for (var i = 0; i < newColumn1Inputs.length; i++) {
      var value = parseFloat(newColumn1Inputs[i].value);
      if (!isNaN(value)) {
        column1Sum += value;
      }
    }

    for (var i = 0; i < newColumn2Inputs.length; i++) {
      var value = parseFloat(newColumn2Inputs[i].value);
      if (!isNaN(value)) {
        column2Sum += value;
      }
    }

    for (var i = 0; i < newColumn3Inputs.length; i++) {
      var value = parseFloat(newColumn3Inputs[i].value);
      if (!isNaN(value)) {
        column3Sum += value;
      }
    }

    document.getElementById('total_1').textContent = column1Sum;
    document.getElementById('total_2').textContent = column2Sum;
    document.getElementById('total_3').textContent = column3Sum;
  }

  // Обработчики событий для изменения значений в существующих input-элементах
  for (var i = 0; i < column1Inputs.length; i++) {
    column1Inputs[i].addEventListener('input', updateSums);
  }

  for (var i = 0; i < column2Inputs.length; i++) {
    column2Inputs[i].addEventListener('input', updateSums);
  }

  for (var i = 0; i < column3Inputs.length; i++) {
    column3Inputs[i].addEventListener('input', updateSums);
  }

  // Обработчики событий для новых input-элементов
  document.addEventListener('input', function (event) {
    var target = event.target;
    if (
      target.matches('input[name^="new_cladiri_"]') ||
      target.matches('input[name^="new_apart_"]') ||
      target.matches('input[name^="new_sup_total_"]')
    ) {
      updateSums();
    }
  });

  // Обработчик события для элементов с классом "txt-c delete-icon-invest"
  var deleteIcons = document.querySelectorAll('.txt-c.delete-icon-invest');
  for (var i = 0; i < deleteIcons.length; i++) {
    deleteIcons[i].addEventListener('click', function (event) {
      var code = this.getAttribute('data-code');
      console.log("Clicked on element with code:", code);
      updateSums(); // Обновляем суммы
    });
  }
});
