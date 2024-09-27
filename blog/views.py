from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group


def home(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html', {'post' : post})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()  # Fetch all posts
        
        


    
        return render(request, 'blog/dashboard.html', {'posts': posts,})
    else:
        return HttpResponseRedirect('/login/')
    

def user_login(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')  # Redirect if the user is already authenticated

    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login Successfully')
                return redirect('/dashboard/')
            else:
                messages.error(request, 'Invalid username or password.')  # Handle authentication failure
        else:
            messages.error(request, 'Invalid form submission.')  # Handle form validation errors
    else:
        form = LoginForm()

    # Always render a response at the end
    return render(request, 'blog/login.html', {'form': form})
    
        

def user_signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            
            messages.success(request,  'Thank You For Joining Us In The Realm Of Humanity')
            form.save() 
    else:
        form = SignUpForm()
    
    return render(request, 'blog/signup.html', {'form' : form})


def user_logout(request):

    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()  # Save the form directly
                return redirect('dashboard')  # Redirect to the dashboard after saving
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')
        
    
    
def update_post(request, id):
    if not request.user.is_authenticated:
        return redirect('/login/')  # Redirect to login if not authenticated

    # Check if the post exists using filter first, and then use get
    post_exists = Post.objects.filter(pk=id).exists()
    if not post_exists:
        return redirect('dashboard')  # Redirect to dashboard if post not found

    post = Post.objects.get(pk=id)  # Use get now that we know the post exists

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # Use the existing post for updating
        if form.is_valid():
            form.save()  # Save the updated post
            return redirect('dashboard')  # Redirect to the dashboard after saving
    else:
        form = PostForm(instance=post)  # Populate the form with existing data

    return render(request, 'blog/updatepost.html', {'form': form})  # Render the update form
    

def delete_post(request, id):
    if request.user.is_authenticated:  # Check if the user is authenticated
        post = Post.objects.get(pk=id)  # Get the post by ID
        post.delete()  # Delete the post
        return redirect('dashboard')  # Redirect to the dashboard
    else:
        return redirect('/login/')  # Redirect to login if not authenticated
