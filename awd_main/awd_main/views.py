from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import render, redirect

from dataentry.tasks import celery_test_task
from awd_main.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm

def home(request):

    return render(request, 'home.html')


def celery_test(request):

    # I want to executing a time consuming task here

    celery_test_task.delay()

    return HttpResponse('<h3>Function executed successfully</h3>')


def register(request):

    if request.method == 'POST':

        form = RegistrationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Registration successfully!')

            return redirect('register')

        else:

            context = {
                'form': form
            }

            return render(request, 'register.html', context=context)

    else:

        form = RegistrationForm()

        context = {
            'form': form
        }

    return render(request, 'register.html', context=context)


def login(request):

    if request.method == 'POST':

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            username = form.cleaned_data['username']

            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('home')

        else:

            messages.error(request, 'Invalid username or password')

            return redirect('login')

    else:

        form = AuthenticationForm()

        context = {
            'form':form
        }

    return render(request, 'login.html', context=context)


def logout(request):

    auth.logout(request)

    return redirect('home')