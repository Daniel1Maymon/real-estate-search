
function handleSubmit(event) {
    event.preventDefault();
    var name = document.getElementById('name').value;
    var luckyNumber = document.getElementById('luckyNumber').value;

    var attributes = "name=" + encodeURIComponent(name) + "&luckyNumber=" + encodeURIComponent(luckyNumber)

    fetch('/submit?' + attributes)
        .then(response => response.text())
        .then(data => {
            document.getElementById('result').innerText = data;
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', function () {
    var inputForm = document.getElementById('myInputForm')

    inputForm.addEventListener('submit', handleSubmit);
});
