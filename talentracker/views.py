from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm

def home(request):
    return render(request, 'home.html')  # Página de inicio

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el usuario en la base de datos
            login(request, user)  # Inicia sesión automáticamente
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})  # Formulario de registro