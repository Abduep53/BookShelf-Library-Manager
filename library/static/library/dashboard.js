// AJAX functionality for updating book status and deleting books

document.addEventListener('DOMContentLoaded', function() {
    
    // Get CSRF token from cookies
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
    
    const csrftoken = getCookie('csrftoken');
    
    // Update book status
    const statusLinks = document.querySelectorAll('.update-status');
    statusLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const bookId = this.dataset.bookId;
            const newStatus = this.dataset.status;
            const card = this.closest('.book-card');
            
            // Send AJAX request
            fetch(`/update/${bookId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `status=${newStatus}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the badge
                    const badge = card.querySelector('.badge');
                    badge.textContent = newStatus;
                    
                    // Update badge color
                    badge.className = 'badge';
                    if (newStatus === 'Reading') {
                        badge.classList.add('bg-warning');
                    } else if (newStatus === 'Completed') {
                        badge.classList.add('bg-success');
                    } else {
                        badge.classList.add('bg-info');
                    }
                    
                    // Show success message
                    showAlert('success', data.message);
                    
                    // Reload page after 1 second to update statistics
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    showAlert('danger', 'Failed to update book status.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showAlert('danger', 'An error occurred while updating the book.');
            });
        });
    });
    
    // Delete book
    const deleteButtons = document.querySelectorAll('.delete-book');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function() {
            const bookId = this.dataset.bookId;
            const card = this.closest('.book-card');
            const bookTitle = card.querySelector('.card-title').textContent;
            
            // Confirm deletion
            if (confirm(`Are you sure you want to delete "${bookTitle}"?`)) {
                // Send AJAX request
                fetch(`/delete/${bookId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken,
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the card with animation
                        card.style.transition = 'opacity 0.3s, transform 0.3s';
                        card.style.opacity = '0';
                        card.style.transform = 'scale(0.8)';
                        
                        setTimeout(() => {
                            card.closest('.col-md-6').remove();
                            showAlert('success', data.message);
                            
                            // Reload page to update statistics
                            setTimeout(() => {
                                location.reload();
                            }, 1000);
                        }, 300);
                    } else {
                        showAlert('danger', 'Failed to delete book.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    showAlert('danger', 'An error occurred while deleting the book.');
                });
            }
        });
    });
    
    // Helper function to show alerts
    function showAlert(type, message) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        const container = document.querySelector('.container.my-5');
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 3 seconds
        setTimeout(() => {
            alertDiv.classList.remove('show');
            setTimeout(() => alertDiv.remove(), 150);
        }, 3000);
    }
});

