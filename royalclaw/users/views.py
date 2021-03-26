from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm
from django.apps import apps


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
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
            user = form.save()
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            messages.success(request, 'Account was created for ' + username)

            # make user a customer
            customerModel = apps.get_model('store', 'Customer')
            customer, created = customerModel.objects.get_or_create(email=email)
            customer.name = username
            # link user to customer
            customer.user = user
            customer.save()

            return redirect('login')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def changePWPage(request):
    form = 1

    context = {'form': form}
    return render(request, 'users/change-pw.html', context)
