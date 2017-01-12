from django.shortcuts import render
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response, redirect
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.core.urlresolvers import reverse


# Create your views here.
def post_list(request):
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    paginator = Paginator(posts_list, 4)  # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        'post_list':posts_list,
        'posts':queryset, 
        "page_request_var": page_request_var,
    }

    return render (request, 'blog/post_list.html',context)

def post_detail (request, slug):
    # posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
        'post_list': posts_list,
    }
    return render(request, 'blog/post_detail.html', context)

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # message.success(reqest, "successfuly created")
            return redirect('post_list',)
    else:
        # message.error(request, "error not created")
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    posts_list = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')[:5]
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    context = {
        'post_list': posts_list,
        'form': form,
        }
    return render(request, 'blog/post_edit.html', context)
