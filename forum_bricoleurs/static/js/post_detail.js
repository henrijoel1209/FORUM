document.addEventListener("DOMContentLoaded", function () {
    // Ajout des gestionnaires d'événements sur les boutons "Like" et "Dislike"
    const likeButtons = document.querySelectorAll('.like-btn');
    const dislikeButtons = document.querySelectorAll('.dislike-btn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = button.getAttribute('data-post-id');
            handleReaction(postId, 'like');
        });
    });

    dislikeButtons.forEach(button => {
        button.addEventListener('click', function () {
            const postId = button.getAttribute('data-post-id');
            handleReaction(postId, 'dislike');
        });
    });

    // Fonction pour envoyer la requête de like/dislike
    function handleReaction(postId, reactionType) {
        fetch(`/posts/${postId}/${reactionType}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById(`like-count-${postId}`).textContent = data.likes;
            document.getElementById(`dislike-count-${postId}`).textContent = data.dislikes;
        })
        .catch(error => console.error('Error:', error));
    }

    // Fonction pour obtenir le CSRF Token (utile pour les requêtes AJAX)
    function getCSRFToken() {
        const cookieValue = document.cookie.match(/csrftoken=([^;]+)/);
        return cookieValue ? cookieValue[1] : '';
    }
});
