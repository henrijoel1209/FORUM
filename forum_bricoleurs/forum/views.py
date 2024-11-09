from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.forms import modelformset_factory
from django.contrib import messages
from django.contrib.auth import get_user_model
import json
from .models import Post, Step, Comment
from .forms import PostForm, StepForm, CommentForm

def home(request):
    User = get_user_model()
    latest_posts = Post.objects.select_related('author').order_by('-created_at')[:5]
    context = {
        'latest_posts': latest_posts,
        'user_count': User.objects.count(),
        'post_count': Post.objects.count(),
        'comment_count': Comment.objects.count(),
    }
    return render(request, 'forum/home.html', context)

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Subscription

from django.db.models import Count

@login_required
def subscribe(request, user_id):
    user_to_subscribe = get_object_or_404(get_user_model(), id=user_id)
    if user_to_subscribe != request.user:
        subscription, created = Subscription.objects.get_or_create(
            subscriber=request.user, 
            subscribed_to=user_to_subscribe
        )
        if created:
            messages.success(request, f"Vous êtes maintenant abonné(e) à {user_to_subscribe.username}.")
    return redirect('profile', username=user_to_subscribe.username)

@login_required
def unsubscribe(request, user_id):
    user_to_unsubscribe = get_object_or_404(get_user_model(), id=user_id)
    Subscription.objects.filter(
        subscriber=request.user, 
        subscribed_to=user_to_unsubscribe
    ).delete()
    messages.success(request, f"Vous vous êtes désabonné(e) de {user_to_unsubscribe.username}.")
    return redirect('profile', username=user_to_unsubscribe.username)


@login_required
def post_create(request):
    StepFormSet = modelformset_factory(Step, form=StepForm, extra=1)
    if request.method == 'POST':
        form = PostForm(request.POST)
        formset = StepFormSet(request.POST, request.FILES, queryset=Step.objects.none())
        if form.is_valid() and formset.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            steps = formset.save(commit=False)
            for i, step in enumerate(steps, 1):
                step.post = post
                step.order = i
                step.save()
            messages.success(request, 'Publication créée avec succès!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
        formset = StepFormSet(queryset=Step.objects.none())
    return render(request, 'forum/post_form.html', {'form': form, 'step_formset': formset})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        messages.error(request, "Vous n'avez pas la permission de modifier cette publication.")
        return redirect('post_detail', pk=pk)
    
    StepFormSet = modelformset_factory(Step, form=StepForm, extra=0)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        formset = StepFormSet(request.POST, request.FILES, queryset=post.steps.all())
        if form.is_valid() and formset.is_valid():
            post = form.save()
            steps = formset.save(commit=False)
            for step in post.steps.all():
                if step not in steps:
                    step.delete()
            for i, step in enumerate(steps, 1):
                step.post = post
                step.order = i
                step.save()
            messages.success(request, 'Publication mise à jour avec succès!')
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
        formset = StepFormSet(queryset=post.steps.all())
    
    return render(request, 'forum/post_form.html', {'form': form, 'step_formset': formset})

# ... autres vues

def post_list(request):
    posts = Post.objects.select_related('author').prefetch_related('likes', 'dislikes').order_by('-created_at')
    return render(request, 'forum/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post.objects.select_related('author').prefetch_related(
        'steps', 'comments__author', 'comments__replies__author'
    ), pk=pk)
    return render(request, 'forum/post_detail.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        post.delete()
        messages.success(request, 'Publication supprimée avec succès!')
        return redirect('post_list')
    messages.error(request, "Vous n'avez pas la permission de supprimer cette publication.")
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Commentaire ajouté avec succès!')
    return redirect('post_detail', pk=post_id)

from django.shortcuts import get_object_or_404, redirect
from .models import Comment

def add_reply(request, comment_id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get("reply_content")
        if content:
            reply = Comment(author=request.user, content=content, parent=comment)
            reply.save()
        return redirect('post_detail', post_id=comment.post.id)
    return redirect('post_detail', post_id=comment.post.id)


@login_required
def handle_reaction(request, post_id, reaction_type):
    post = get_object_or_404(Post, id=post_id)
    if reaction_type == 'like':
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            post.dislikes.remove(request.user)
    else:
        if request.user in post.dislikes.all():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)
            post.likes.remove(request.user)
    
    return JsonResponse({
        'likes': post.likes.count(),
        'dislikes': post.dislikes.count()
    })
