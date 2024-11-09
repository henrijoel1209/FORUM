from django.urls import path
from .views import home, post_list, post_detail, post_create, delete_post, add_comment, handle_reaction, post_edit, subscribe, unsubscribe, add_reply
urlpatterns = [
    path('', home, name='home'),
    path('posts/', post_list, name='post_list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/create/', post_create, name='post_create'),
    path('posts/<int:pk>/edit/', post_edit, name='post_edit'),  # Utilisation de pk ici
    path('posts/<int:post_id>/delete/', delete_post, name='delete_post'),
    path('comments/<int:post_id>/add/', add_comment, name='add_comment'),
    path('posts/<int:post_id>/<str:reaction_type>/', handle_reaction, name='handle_reaction'),
    path('subscribe/<int:user_id>/', subscribe, name='subscribe'),
    path('unsubscribe/<int:user_id>/', unsubscribe, name='unsubscribe'),
    path('add-reply/<int:comment_id>/',add_reply, name='add_reply')
]
