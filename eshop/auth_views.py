from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Webuser


def login(request):
    return render(request, 'auth/login.html')

def authenticate(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if not user:
        return redirect('login')
    auth.login(request, user)
    return redirect('index')

def signup(request):
    return render(request, 'auth/signup.html')

def signup_submit(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    try:
        user = User.objects.create_user(username=username, password=password)
        real_user = Webuser(ori_user = user,
                            is_owner = True,
                            nickname = "",
                            gender = False,
                            age = 1,)
        real_user.save()
        return redirect('login')
    except:
        return redirect('signup')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')

def user_info(request):
    real_user  = get_object_or_404(Webuser, pk = request.user.real_user.id)
    return render(request, 'base/user_info.html', {'real_user' : real_user})

def change_user_info(request):
    real_user  = get_object_or_404(Webuser, pk = request.user.real_user.id)
    return render(request, 'customer/change_user_info.html', {'real_user': real_user})

def save_user_info(request):
    real_user  = get_object_or_404(Webuser, pk = request.user.real_user.id)
    real_user.nickname = request.POST.get("nickname")
    real_user.gender = True if request.POST.get("gender") == "Male" else False
    real_user.age = request.POST.get("age")
    real_user.email = request.POST.get("email")
    if real_user.photo:
        real_user.photo.delete()
    real_user.photo = request.FILES.get("photo")
    real_user.save()
    return render(request, 'customer/save_user_info.html', {'real_user': real_user})
