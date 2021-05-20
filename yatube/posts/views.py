from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Group, Follow
from .forms import PostForm, CommentForm
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()


def post_paginator(request, post_list):
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return page, paginator


def index(request):
    post_list = Post.objects.select_related('group').order_by('-pub_date')
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'index.html', {'page': page})


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.select_related('group').all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, 'page': page, })


@login_required
def new_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('index')
        return render(request, 'new.html', {'form': form})
    form = PostForm(request.POST or None, files=request.FILES or None)
    return render(request, 'new.html', {'form': form})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm()
    comments = post.comments.all()
    author = post.author
    if author.username == username:
        return render(request, 'post.html', {
            'post': post,
            'author': author,
            'form': form,
            'comments': comments,
        })


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = post.author
    # проверка на владельца поста.
    if request.user != author:
        return redirect(reverse('post', kwargs={'username': username,
                                                "post_id": post_id
                                                }))

    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if form.is_valid():
        post = form.save(commit=False)
        post.save()
        return redirect(reverse('post', kwargs={'username': username,
                                                'post_id': post_id}))

    return render(request, 'post_edit.html', {'form': form,
                                              'post': post,
                                              'is_edit': True})


@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username=username, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.POST and form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        form.save()
    return redirect('post', username=username, post_id=post_id)


@login_required
def follow_index(request):
    post_list = Post.objects.filter(author__following__user=request.user)
    page, paginator = post_paginator(request, post_list)
    return render(request, 'follow.html',
                  {'page': page, 'paginator': paginator})


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('profile', username=username)
    



@login_required
def profile_unfollow(request, username):
    follower = get_object_or_404(Follow,
                                 user=request.user,
                                 author__username=username)
    follower.delete()

    return redirect('profile', username=username)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    following = request.user.is_authenticated and Follow.objects.filter(
        user=request.user, author=author).exists()
    following_count = author.follower.count()
    followers_count = author.following.count()
    post_list = author.posts.all()
    page, paginator = post_paginator(request, post_list)
    return render(request, 'profile.html', {
        'page': page,
        'paginator': paginator,
        'profile': author,
        'following': following,
        'following_count': following_count,
        'followers_count': followers_count,
    })


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404)


def server_error(request):
    return render(request, "misc/500.html", status=500)
