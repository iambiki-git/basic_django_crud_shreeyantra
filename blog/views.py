from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm  # Assuming you have a form for Post model



# Create your views here.
def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        
        if user is None:
            messages.error(request, "Invalid credentials, please try again")
            return redirect('login')  # Redirect back to the login page
        
        # Log the user in
        login(request, user)
        return redirect('profile')  # Redirect to the homepage or dashboard
    
    return render(request, 'login.html')


def registration_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Validate that passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('registration')  # Redirect back to registration page
        
        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('registration')  # Redirect back to registration page
        
        # Create a new user if everything is valid
        try:
            user = User.objects.create_user(
                email=email, 
                username=email, 
                password=password
            )
            user.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('registration')  # Redirect back to registration page
        
        
    return render(request, 'registration.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        # Create a new post or update the user's existing post
        if title and content:
            # Create a new post (or update the existing one)
            post = Post.objects.create(
                title=title,
                content=content,
                author=request.user
            )
            # Optionally, redirect to the profile or post detail page
            return redirect('profile')  # Redirect to the profile page after saving

    # Optionally, retrieve existing posts by the logged-in user
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'profile.html', {'posts': posts})


def delete_post(request, post_id):
    # Get the post by ID
    post = Post.objects.get(id=post_id)

    # Check if the post belongs to the logged-in user
    if post.author == request.user:
        post.delete()
        messages.success(request, "Post deleted successfully")
    else:
        messages.error(request, "You are not authorized to delete this post")

    return redirect('profile')  # Redirect back to the profile page



def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == "POST":
        # Process the form with the updated data
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect('profile')  # Redirect to the profile or post list page
    else:
        # Initial form with the current post's data
        form = PostForm(instance=post)
    
    return render(request, 'edit_post.html', {'form': form})
