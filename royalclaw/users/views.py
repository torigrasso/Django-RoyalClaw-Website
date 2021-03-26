from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('username')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # DOES NOT WORK
            redirect("{% url 'home' %}")
        else:
            messages.info(request, 'Username OR Password is incorrect')
    context = {}
    return render(request, 'users/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # django validates user specifications already
        if form.is_valid():
            # save user
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'users/register.html', context)
