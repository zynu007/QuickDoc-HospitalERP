from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import BlogPost, Category
from .forms import BlogPostForm
from django.contrib import messages



@login_required
def blog_home(request):
    category = request.GET.get('category', '')
    
    if category and category in dict(Category.choices).keys():
        posts = BlogPost.objects.filter(is_published=True, category=category)
    else:
        posts = BlogPost.objects.filter(is_published=True)
    
    context = {
        'posts': posts,
        'categories': Category.choices,
        'selected_category': category
    }
    return render(request, 'blog/blog_home.html', context)

@login_required
def blog_detail(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is author for draft posts
    if not post.is_published and post.author != request.user:
        return HttpResponseForbidden("You don't have permission to view this post")
    
    return render(request, 'blog/blog_detail.html', {'post': post})

@login_required
def blog_create(request):
    # Check if user is a doctor
    if not hasattr(request.user, 'is_doctor') or not request.user.is_doctor:
        messages.error(request, "Only doctors can create blog posts")
        return redirect('blog_home')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Check if publish button was clicked
            if 'publish' in request.POST:
                post.is_published = True
            
            post.save()
            messages.success(request, "Blog post created successfully")
            return redirect('blog_home')
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/blog_create.html', {'form': form})

@login_required
def my_posts(request):
    # Check if user is a doctor
    if not hasattr(request.user, 'is_doctor') or not request.user.is_doctor:
        return redirect('blog_home')
    
    posts = BlogPost.objects.filter(author=request.user)
    return render(request, 'blog/my_posts.html', {'posts': posts})

@login_required
def publish_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Verify user is the author
    if post.author != request.user:
        return HttpResponseForbidden("You don't have permission to publish this post")
    
    post.is_published = True
    post.save()
    messages.success(request, "Blog post published successfully")
    return redirect('my_posts')