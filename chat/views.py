from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ChatRoom, Message, UserProfile
from .forms import UserRegisterForm, UserLoginForm, UserProfileForm, UserUpdateForm


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create UserProfile for new user
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = UserRegisterForm()
    
    return render(request, 'chat/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'chat/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


@login_required(login_url='login')
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile
    }
    return render(request, 'chat/profile.html', context)


@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            ChatRoom.objects.get_or_create(name=room_name)
            return redirect('room', room_name=room_name)
    
    chatrooms = ChatRoom.objects.all().order_by('-created_at')
    return render(request, 'chat/index.html', {'chatrooms': chatrooms})


@login_required(login_url='login')
def room(request, room_name):
    chatroom, created = ChatRoom.objects.get_or_create(name=room_name)
    messages_list = Message.objects.filter(chat_room=chatroom).order_by('timestamp')
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages_list,
        'chatroom': chatroom
    })


@login_required(login_url='login')
def send_message(request, room_name):
    if request.method != 'POST':
        return redirect('room', room_name=room_name)

    chatroom = get_object_or_404(ChatRoom, name=room_name)
    content = request.POST.get('content', '').strip()
    if not content:
        messages.error(request, 'Cannot send empty message.')
        return redirect('room', room_name=room_name)

    message = Message.objects.create(chat_room=chatroom, user=request.user, content=content)

    # If AJAX, return JSON for client-side updates
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'id': message.id,
            'user': request.user.username,
            'content': message.content,
            'timestamp': message.timestamp.isoformat(),
        })

    return redirect('room', room_name=room_name)


@login_required(login_url='login')
def toggle_theme(request):
    # Toggle the user's theme preference between 'light' and 'dark'
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    new_theme = 'dark' if user_profile.theme == 'light' else 'light'
    user_profile.theme = new_theme
    user_profile.save()

    return JsonResponse({'theme': new_theme})