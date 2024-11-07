from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm, UserUpdateForm

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    is_own_profile = request.user == user
    is_following = request.user.is_authenticated and request.user.following.filter(id=user.id).exists()

    # Handle avatar URL safely
    avatar_url = user.avatar.url if user.avatar and hasattr(user.avatar, 'url') else '/static/images/default-avatar.png'
    
    context = {
        'profile_user': user,
        'is_own_profile': is_own_profile,
        'is_following': is_following,
        'posts': user.post_set.order_by('-created_at'),  # Assurez-vous que Post existe
        'avatar_url': avatar_url,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)  # Récupérer l'utilisateur par nom d'utilisateur

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour avec succès!')
            return redirect('profile', username=user.username)
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'users/profile_edit.html', {'form': form, 'profile_user': user})

@login_required
def follow_toggle(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user == user_to_follow:
        messages.error(request, "Vous ne pouvez pas vous suivre vous-même.")
        return redirect('profile', username=username)
    
    if request.user.following.filter(id=user_to_follow.id).exists():
        request.user.unfollow(user_to_follow)
        messages.success(request, f"Vous ne suivez plus {username}.")
    else:
        request.user.follow(user_to_follow)
        messages.success(request, f"Vous suivez maintenant {username}.")
    
    return redirect('profile', username=username)
