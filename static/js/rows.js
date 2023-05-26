function addRow() {
    var template = document.getElementById('new-row-template');
    var table = document.getElementById("tableReports");
    var newRow = template.cloneNode(true);
    newRow.removeAttribute('id');
    newRow.style.display = '';
    table.appendChild(newRow);
}