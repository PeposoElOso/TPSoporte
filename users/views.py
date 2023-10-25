
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from users.forms import RegisterForm
from users.models import User
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404, redirect
from django.views import View
# Create your views here.


class UserRegistration(FormView):
    template_name = 'users/registration.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:success')
    
    def form_valid(self, form):
        form.save()
        return super(UserRegistration, self).form_valid(form)
    
    


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    
    def get_object(self, queryset=None):
        user_id = self.kwargs.get('user_id')  # Obtén el user_id desde los parámetros de la URL
        return get_object_or_404(User, id=user_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        return context
    
      
def contador(request, user_id):
    user = User.objects.get(pk=user_id)
    
    return render(request, {'user': user})




class seguir_usuario(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        if self.request.user in user.followers.all():
            # Si el usuario actual ya está siguiendo al usuario, entonces dejaremos de seguirlo
            self.request.user.followers.remove(user)
        else:
            # Si el usuario actual no está siguiendo al usuario, lo seguiremos
            self.request.user.followers.add(user)
        return redirect('users:profile', user_id=user.id)