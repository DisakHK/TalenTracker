from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'home.html')  # Página de inicio

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la página de inicio después del login
        else:
            # Mensaje de error si las credenciales son incorrectas
            return render(request, 'talentracker/iniciar_sesion.html', {'error': 'Usuario o contraseña incorrectos'})
    return render(request, 'iniciar_sesion.html')