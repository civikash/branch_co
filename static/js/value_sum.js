window.addEventListener('load', function() {
    var column1Sum = 0;
    var column2Sum = 0;
    var column3Sum = 0;
  
    var column1Inputs = document.querySelectorAll('input[name^="cladiri_"]');
    for (var i = 0; i < column1Inputs.length; i++) {
      column1Inputs[i].addEventListener('input', updateSums);
      var value = parseFloat(column1Inputs[i].value);
      if (!isNaN(value)) {
        column1Sum += value;
      }
    }
  
    var column2Inputs = document.querySelectorAll('input[name^="apart_"]');
    for (var i = 0; i < column2Inputs.length; i++) {
      column2Inputs[i].addEventListener('input', updateSums);
      var value = parseFloat(column2Inputs[i].value);
      if (!isNaN(value)) {
        column2Sum += value;
      }
    }
  
    var column3Inputs = document.querySelectorAll('input[name^="sup_total_"]');
    for (var i = 0; i < column3Inputs.length; i++) {
      column3Inputs[i].addEventListener('input', updateSums);
      var value = parseFloat(column3Inputs[i].value);
      if (!isNaN(value)) {
        column3Sum += value;
      }
    }
  
    document.getElementById('total_1').textContent = column1Sum;
    document.getElementById('total_2').textContent = column2Sum;
    document.getElementById('total_3').textContent = column3Sum;
  
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
  
      document.getElementById('total_1').textContent = column1Sum;
      document.getElementById('total_2').textContent = column2Sum;
      document.getElementById('total_3').textContent = column3Sum;
    }
  });
  