from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is None:
            messages.error(request=request, message='Username password is incorrect')
            return redirect('login')
        auth.login(request=request, user=user)
        messages.success(request=request, message='You have successfully logged in')
        return redirect('dashboard')
    return render(request=request, template_name='accounts/login.html')


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords match
        if password != password2:
            messages.error(request=request, message='Passwords do not match')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request=request, message='User already exists')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request=request, message="Email already used")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password,
                                        email=email, first_name=first_name,
                                        last_name=last_name)
        user.save()
        messages.success(request=request, message='You have successfully registered')
        return redirect('login')
    return render(request=request, template_name='accounts/register.html')


@login_required(login_url='login')
def dashboard(request):
    query_listings = Contact.objects.filter(user_id=request.user.id).all()
    context = {
        'query_listings': query_listings
    }
    return render(request=request, template_name='accounts/dashboard.html', context=context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request=request)
        messages.success(request=request, message='You have successfully logged out')
        return redirect('index')
    return redirect('login')
