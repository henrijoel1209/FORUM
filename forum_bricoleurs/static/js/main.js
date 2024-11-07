// Notifications handling
document.addEventListener('DOMContentLoaded', function() {
    const notificationDropdown = document.getElementById('notificationsDropdown');
    const notificationsList = document.getElementById('notifications-list');
    
    if (notificationDropdown) {
        // Update notifications count
        function updateNotificationsCount() {
            fetch('/notifications/api/unread_count/')
                .then(response => response.json())
                .then(data => {
                    const badge = document.getElementById('notification-count');
                    if (data.count > 0) {
                        badge.textContent = data.count;
                        badge.style.display = 'inline';
                    } else {
                        badge.style.display = 'none';
                    }
                });
        }

        // Mark notifications as read
        notificationDropdown.addEventListener('click', function() {
            fetch('/notifications/mark-all-as-read/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                }
            }).then(() => {
                updateNotificationsCount();
            });
        });

        // Update notifications periodically
        setInterval(updateNotificationsCount, 30000);
    }
});

// CSRF Token helper
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