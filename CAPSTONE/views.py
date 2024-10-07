from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

 
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully.')
            return render(request, 'CAPSTONE/signup.html')
    else:
        form = UserCreationForm()
    return render(request, 'CAPSTONE/signup.html', {'form': form})
 
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'App/app.html') 
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'CAPSTONE/signin.html')
 