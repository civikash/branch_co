var next_auto_increment_value = 0;
window.addEventListener('load', function () {


  var column1Sum = 0;
  var column2Sum = 0;
  var column3Sum = 0;

  var column1Inputs = document.querySelectorAll('input[name^="cladiri_"]');
  var column2Inputs = document.querySelectorAll('input[name^="apart_"]');
  var column3Inputs = document.querySelectorAll('input[name^="sup_total_"]');

  updateSums();
  var lastAutoIncrementedValue = 1;
  var next_auto_increment_value = 1;

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
    var autoIncrementCell = document.querySelector('.auto-increment-cell');
    
    if (autoIncrementCell) {
      lastAutoIncrementedValue++;
      autoIncrementCell.textContent = lastAutoIncrementedValue;
    }

    return lastAutoIncrementedValue;
  }

  function addNewRow() {
    // Get the template row
    var templateRow = document.getElementById('newRtemplate');
  
    // Clone the template row
    var newRow = templateRow.cloneNode(true);
  
    // Remove the 'id' attribute from the cloned row to prevent duplicate IDs in the DOM
    newRow.removeAttribute('id');
  
    // Update the auto-incremented value
    var autoIncrementCell = newRow.querySelector('.auto-increment-cell');
    if (autoIncrementCell) {
      next_auto_increment_value++; // Increment before adding the new row
      var newCodulRindInput = document.createElement('input');
      newCodulRindInput.type = 'text';
      newCodulRindInput.className = 'tb-input w-full';
      newCodulRindInput.step = 'any';
      newCodulRindInput.name = 'new_codul_rind_';
      newCodulRindInput.value = next_auto_increment_value;
  
      // Remove the existing content from the auto-increment-cell
      autoIncrementCell.innerHTML = '';
  
      // Append the new input element to the auto-increment-cell
      autoIncrementCell.appendChild(newCodulRindInput);
    }
  
    // Set the display property of the cloned row to an empty string to make it visible
    newRow.style.display = '';
  
    // Append the new row to the table
    var tableBody = document.getElementById('tableBody'); // Replace 'tableBody' with the actual ID of the table body
    if (tableBody) {
      tableBody.appendChild(newRow);
    }
  
    updateSums();
  }
  
  
  
  
  

  lastAutoIncrementedValue = updateSums();

  for (var i = 0; i < column1Inputs.length; i++) {
    column1Inputs[i].addEventListener('input', updateSums);
  }

  for (var i = 0; i < column2Inputs.length; i++) {
    column2Inputs[i].addEventListener('input', updateSums);
  }

  for (var i = 0; i < column3Inputs.length; i++) {
    column3Inputs[i].addEventListener('input', updateSums);
  }

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

  var deleteIcons = document.querySelectorAll('.txt-c.delete-icon-invest');
  for (var i = 0; i < deleteIcons.length; i++) {
    deleteIcons[i].addEventListener('click', function (event) {
      var code = this.getAttribute('data-code');
      console.log(":", code);
      updateSums();
    });
  }

  var addButton = document.getElementById('add-row-button'); // Replace 'add-row-button' with the actual ID of your button
  if (addButton) {
    addButton.addEventListener('click', function (event) {
      addNewRow();
    });
  }
});
