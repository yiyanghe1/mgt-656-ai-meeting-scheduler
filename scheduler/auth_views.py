from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import SignUpForm


class CustomLoginView(LoginView):
    """Custom login view."""
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add Bootstrap classes to form fields
        form.fields['username'].widget.attrs.update({'class': 'form-control'})
        form.fields['password'].widget.attrs.update({'class': 'form-control'})
        return form


class CustomLogoutView(LogoutView):
    """Custom logout view."""
    next_page = '/'


class SignUpView(CreateView):
    """User registration view."""
    form_class = SignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        """Log the user in after successful registration."""
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect('dashboard')  # Redirect to dashboard after signup

    def get(self, request, *args, **kwargs):
        """Redirect to dashboard if user is already authenticated."""
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)
