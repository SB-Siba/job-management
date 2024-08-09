document.getElementById('editForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    var form = event.target;
    var formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': form.querySelector('input[name="csrfmiddlewaretoken"]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            var editModal = bootstrap.Modal.getInstance(document.getElementById('editModal'));
            editModal.hide();

            var messageDiv = document.getElementById('successMessage');
            messageDiv.innerText = data.message;
            messageDiv.style.display = 'block';
            
            setTimeout(() => {
                messageDiv.style.display = 'none';
                location.reload();
            }, 2000);
        } else {
            console.error('Update failed:', data.errors || 'Unknown error');
            alert('An error occurred while updating the client.');
        }
    })
    .catch(error => console.error('Error:', error));
});
