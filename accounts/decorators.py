from django.shortcuts import redirect
from django.contrib import messages

def donneur_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'donneur'):
            messages.error(request, 'Accès réservé aux donneurs.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def hopital_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'hopital'):
            messages.error(request, 'Accès réservé aux hôpitaux.')
            return redirect('home')
        hopital = request.user.hopital
        if not hopital.valide:
            messages.warning(request, 'Votre compte est en attente de validation par l\'administrateur.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_staff:
            messages.error(request, 'Accès réservé aux administrateurs.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper