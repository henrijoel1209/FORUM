from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .models import Message

User = get_user_model()

@login_required
def chat_list(request):
    chat_users = User.objects.filter(
        Q(sent_messages__recipient=request.user) | 
        Q(received_messages__sender=request.user)
    ).distinct()
    
    return render(request, 'chat/chat_list.html', {'chat_users': chat_users})

@login_required
def chat_detail(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=other_user) |
        Q(sender=other_user, recipient=request.user)
    ).order_by('timestamp')
    
    # Marquer les messages comme lus
    unread_messages = messages.filter(recipient=request.user, is_read=False)
    unread_messages.update(is_read=True)
    
    return render(request, 'chat/chat_detail.html', {
        'other_user': other_user,
        'messages': messages
    })
