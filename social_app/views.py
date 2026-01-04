from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm
from django.contrib import messages

@login_required
def feed(request):
    # Pobieramy wszystkie posty użytkowników, których obserwuje current user
    user_profile = request.user.profile
    following_users = [p.user for p in user_profile.following.all()]
    
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    return render(request, 'social_app/feed.html', {'posts': posts})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
    return redirect('feed')

@login_required
def follow_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    profile = request.user.profile
    target_profile = target_user.profile  # <- konieczne
    if target_profile in profile.following.all():
        profile.following.remove(target_profile)
    else:
        profile.following.add(target_profile)
    return redirect('feed')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Konto utworzone! Możesz się teraz zalogować.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'social_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = LoginForm()
    return render(request, 'social_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # przypisanie aktualnego użytkownika
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request, 'social_app/create_post.html', {'form': form})

@login_required
def toggle_follow(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    current_profile = request.user.profile
    target_profile = target_user.profile

    if target_profile in current_profile.following.all():
        current_profile.following.remove(target_profile)
    else:
        current_profile.following.add(target_profile)

    return redirect('user_list')  # po wykonaniu akcji wraca do listy użytkowników

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # nie pokazuj siebie
    return render(request, 'social_app/user_list.html', {'users': users})
