from django.shortcuts import redirect, render, get_object_or_404
from .models import Author, Category, Post, Comment, Reply
from .utils import update_views
from .forms import PostForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .ForbiddenWord import ForbiddenWord
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
    forums = Category.objects.all()
    forum_start_date = datetime.strptime("2023-08-11", "%Y-%m-%d")  # Replace with your start date
    today = datetime.now()
    days = (today - forum_start_date).days
    num_posts = Post.objects.all().count()
    num_users = User.objects.all().count()
    try:
        last_post = Post.objects.latest("date")
    except:
        last_post = 0

    context = {
        "forums":forums,
        "num_posts":num_posts,
        "num_users":num_users,
        "last_post":last_post,
        "days":days,
    }
    return render(request, "home.html", context)

def posts(request,slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved = True, categories = category)
    paginator = Paginator(posts, 5)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {"posts":posts}
    return render(request, "posts.html", context)


def post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if "comment-form" in request.POST:
        try:
            author = Author.objects.get(user=request.user)
        except:
            return redirect("update_profile")
        comment = request.POST.get("content")
        new_comment, created = Comment.objects.get_or_create(user=author, content=comment, account = str(request.user))
        post.comments.add(new_comment.id)

    if "reply-form" in request.POST:
        try:
            author = Author.objects.get(user=request.user)
        except:
            return redirect("update_profile")
        reply = request.POST.get("reply")
        commenr_id = request.POST.get("comment-id")
        comment_obj = Comment.objects.get(id=commenr_id)
        new_reply, created = Reply.objects.get_or_create(user=author, content=reply, account = str(request.user))
        comment_obj.replies.add(new_reply.id)

    context = {"post":post}
    update_views(request, post)
    return render(request, "post.html", context)

@login_required
def createpost(request):
    form = PostForm(request.POST or None)
    context = {}
    if request.method == "POST":
        if form.is_valid():
            try:
                author = Author.objects.get(user=request.user)
            except:
                return redirect("update_profile")
            new_post = form.save(commit=False)
            new_post.account = str(request.user)
            new_post.user = author
            new_post.save()
            # Now, associate the categories and tags from the form
            categories = form.cleaned_data['categories']  # Assuming 'categories' is a field in your form
            new_post.categories.set(categories)  # Set the categories

            tags = form.cleaned_data['tags']  # Assuming 'tags' is a field in your form
            new_post.tags.set(*tags)  # Set the tags using the unpacking operator *

            return redirect("index")
    context.update({
        "form": form,
        "title": "Create New Post"
    })
    return render(request, "createpost.html", context)
