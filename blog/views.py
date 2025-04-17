from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now

from .models import Post, Category
from .forms import PostForm, RegisterForm


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2
    return {'cats1': all[:half], 'cats2': all[half:]}


def index(request):
    posts = Post.objects.all().order_by('-published_date')
    # posts = Post.objects.filter(title__contains='django1')
    # posts = Post.objects.filter(published_date__year=2025)
    # posts = Post.objects.filter(published_date__month=1, published_date__year=2024)
    # posts = Post.objects.filter(category__name__exact="django")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, title):
    post = get_object_or_404(Post, slug=title)
    context = {'post': post}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def category(request, name):
    c = get_object_or_404(Category, name=name)
    posts = Post.objects.filter(category=c).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            return index(request)
    create_form = PostForm()
    context = {'create_form': create_form}
    context.update(get_categories())
    return render(request, "blog/create.html", context)


def custom_logout(request):
    logout(request)
    return redirect('index')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    context = {"form": form}
    context.update(get_categories())
    return render(request, "blog/register.html", context)
