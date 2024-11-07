document.addEventListener("DOMContentLoaded", function () {
    // Ajouter l'événement de clic pour les boutons de like
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function () {
            let postId = this.getAttribute('data-post-id');
            
            // Envoyer la requête AJAX pour le like
            fetch("{% url 'toggle_like' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    post_id: postId,
                    action: 'like'
                })
            })
            .then(response => response.json())
            .then(data => {
                // Mettre à jour les compteurs de like et de dislike
                document.querySelector(`#like-count-${postId}`).textContent = data.likes;
                document.querySelector(`#dislike-count-${postId}`).textContent = data.dislikes;
            })
            .catch(error => console.log('Error:', error));
        });
    });

    // Ajouter l'événement de clic pour les boutons de dislike
    document.querySelectorAll('.dislike-btn').forEach(button => {
        button.addEventListener('click', function () {
            let postId = this.getAttribute('data-post-id');
            
            // Envoyer la requête AJAX pour le dislike
            fetch("{% url 'toggle_like' %}", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    post_id: postId,
                    action: 'dislike'
                })
            })
            .then(response => response.json())
            .then(data => {
                // Mettre à jour les compteurs de like et de dislike
                document.querySelector(`#like-count-${postId}`).textContent = data.likes;
                document.querySelector(`#dislike-count-${postId}`).textContent = data.dislikes;
            })
            .catch(error => console.log('Error:', error));
        });
    });
});
// Fonction pour gérer la réponse aux commentaires
document.querySelectorAll('.reply-btn').forEach(button => {
    button.addEventListener('click', function() {
        const commentId = this.getAttribute('data-comment-id');
        const replyContent = prompt('Votre réponse :');

        if (replyContent) {
            fetch(`/add-reply/${commentId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name="csrfmiddlewaretoken"]').value,
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `content=${replyContent}`
            })
            .then(response => response.json())
            .then(data => {
                // Ajoute la nouvelle réponse dans la section des réponses
                const repliesContainer = this.closest('.comment').querySelector('.replies');
                const replyHtml = `
                    <div class="reply ms-4 mt-2">
                        <div class="d-flex gap-2 align-items-start">
                            <img src="/static/images/default-avatar.png" alt="${data.author}" class="rounded-circle" width="24" height="24">
                            <div>
                                <div class="d-flex justify-content-between">
                                    <strong>${data.author}</strong>
                                    <small class="text-muted">${data.created_at}</small>
                                </div>
                                <p class="mb-0">${data.content}</p>
                            </div>
                        </div>
                    </div>
                `;
                repliesContainer.innerHTML += replyHtml;
            });
        }
    });
});
