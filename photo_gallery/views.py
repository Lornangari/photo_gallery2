from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from .models import Photo, Tag
from .forms import PhotoForm
from django.contrib.auth.decorators import login_required



def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please fix the errors.")
    else:
        form = RegisterForm()
    return render(request, 'photo_gallery/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'photo_gallery/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')




def home_view(request):
    return render(request, 'photo_gallery/home.html')

@login_required
def profile_view(request):
    profile = request.user.profile
    return render(request, 'photo_gallery/profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'photo_gallery/edit_profile.html', {'form': form})

def gallery_view(request):
    tag = request.GET.get('tag')
    if tag:
        photos = Photo.objects.filter(tags__name=tag)
    else:
        photos = Photo.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    return render(request, 'photo_gallery/gallery.html', {'photos': photos, 'tags': tags})

@login_required
def upload_photo_view(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            form.save_m2m()
            messages.success(request, "Photo uploaded successfully!")
            return redirect('gallery')
    else:
        form = PhotoForm()
    return render(request, 'photo_gallery/upload.html', {'form': form})

@login_required
def toggle_like_view(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('gallery')
