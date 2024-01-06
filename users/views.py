from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # creating a user, hashes password automatically
            form.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form': form, 'errors': form.errors})
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        # 'request.POST' contains the data that the user has entered into the form
        # 'request' checks form validation, ie verifies the authentication backend and checking if the user is active
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("transaction-list")
            else:
                messages.error(request, "Invalid username or password")
        else:
            return render(request, 'users/login.html', {'form': form, 'errors': form.errors})
    form = AuthenticationForm()
    return render(request, "users/login.html", {'form': form})


def logout_view(request):
    logout(request)
    return redirect("login")
