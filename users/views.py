from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from carts.models import Carts
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

class UserLoginview(LoginView):
  template_name = 'users/login.html'
  form_class = UserLoginForm

  def get_success_url(self):
     return reverse_lazy("main:index")

  def form_valid(self, form):
     session_key = self.request.session.session_key
     user = form.get_user()
     if user:
        auth.login(self.request, user)
        if session_key:
           forgot_cart = Carts.objects.filter(user=user)
           if forgot_cart.exists():
              forgot_cart.delete() 
           Carts.objects.filter(session_key=session_key).update(user=user)
        messages.success(self.request, f"{user.username}, Вы вошли в аккаунт")
        return HttpResponseRedirect(self.get_success_url())


  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Авторизация'
      return context


class UserRegistrationView(CreateView):
  template_name = 'users/registration.html'
  form_class = UserRegistrationForm
  success_url = reverse_lazy("users:profile")


  def form_valid(self, form):
     session_key = self.request.session.session_key
     user = form.instance
     if user:
        form.save()
        auth.login(self.request, user)
        if session_key:
           Carts.objects.filter(session_key=session_key).update(user=user)
           
        messages.success(self.request, f"{user.username}, Вы успешно зарегистрированы и вошли в аккаунт")
        return HttpResponseRedirect(self.success_url)
  

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Регистрация'
      return context

class UserProfileView(UpdateView):
  template_name = 'users/profile.html'
  form_class = UserProfileForm
  success_url = reverse_lazy("users:profile")
  
  def get_object(self, queryset = ...):
     return self.request.user

  def form_valid(self, form):
        messages.success(self.request, "Профайл успешно обновлен")
        return super().form_valid(form)
    
  def form_invalid(self, form):
        messages.error(self.request, "Произошла ошибка")
        return super().form_invalid(form)
  

  def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      context["title"] = 'Профиль'
      return context
  
@login_required
def logout(request):
  messages.success(request, f"{request.user.username}, Вы успешно вышли из аккаунта")
  auth.logout(request)
  return redirect(reverse_lazy('main:index'))

class UserCartView(TemplateView):
   template_name = 'users/users_cart.html'
   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       context["title"] = 'Корзина'
       return context
   