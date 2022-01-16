from django.contrib import messages, auth
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User


def signup(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(username.strip()) == 0 or len(email.strip()) == 0 or len(password.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Preencha todos os dados')
            return redirect('/auth/signup')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um usuário com esse nome cadastrado')
            return redirect('/auth/signup')

        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')
            return redirect('/auth/login')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/signup')


def login(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')
    elif request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            return redirect('/')


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect('/auth/login')
