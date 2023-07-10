from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages, auth
from .forms import RegisterationForm
from .models import Account
from django.contrib.auth.decorators import login_required

# Create your views here.


def register_view(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split('@')[0]
            print(first_name, last_name, email, password, username)
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.save()
            messages.success(request, "Registraion Successfull")
            return redirect('register')

    else:
        print("else block")
        form = RegisterationForm()
    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    messages.success(request, "logged out successfully")
    return redirect('login')
