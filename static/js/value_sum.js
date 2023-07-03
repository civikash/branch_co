window.addEventListener('load', function () {
  var column1Inputs = document.querySelectorAll('input[name^="cladiri_"]');
  var column2Inputs = document.querySelectorAll('input[name^="apart_"]');
  var column3Inputs = document.querySelectorAll('input[name^="sup_total_"]');
  var deleteButtons = document.querySelectorAll('.delete-icon-invest');

  function updateSums() {
    var column1Sum = 0;
    var column2Sum = 0;
    var column3Sum = 0;

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

    document.getElementById('total_1').textContent = column1Sum;
    document.getElementById('total_2').textContent = column2Sum;
    document.getElementById('total_3').textContent = column3Sum;
  }

  function deleteRowAndRefresh(event) {
    var code = event.target.parentElement.getAttribute('data-code');
    updateSums();
  }

  function addInputListener(input) {
    input.addEventListener('input', updateSums);
  }

  deleteButtons.forEach(function (button) {
    button.addEventListener('click', deleteRowAndRefresh);
  });

  // Добавляем обработчик событий для существующих элементов
  for (var i = 0; i < column1Inputs.length; i++) {
    addInputListener(column1Inputs[i]);
  }

  for (var i = 0; i < column2Inputs.length; i++) {
    addInputListener(column2Inputs[i]);
  }

  for (var i = 0; i < column3Inputs.length; i++) {
    addInputListener(column3Inputs[i]);
  }

  // Добавляем обработчик событий для новых элементов после их добавления
  function addNewRowEventHandlers() {
    var parentContainer = document.getElementById('new-row-template');
    var newCladiriInputs = parentContainer.querySelectorAll('input[name^="new_cladiri_"]');

    for (var i = 0; i < newCladiriInputs.length; i++) {
      addInputListener(newCladiriInputs[i]);
    }

    var newDeleteButtons = parentContainer.querySelectorAll('.delete-icon-invest');
    newDeleteButtons.forEach(function (button) {
      button.addEventListener('click', deleteRowAndRefresh);
    });
  }

  addNewRowEventHandlers();

  // Вызываем функцию updateSums, чтобы отобразить начальные значения сумм
  updateSums();
});
