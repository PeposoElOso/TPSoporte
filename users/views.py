
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from users.forms import RegisterForm
from users.models import User
from django.views import generic, View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView



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
        
        return self.request.user
      
def contador(request, user_id):
    user = User.objects.get(pk=user_id)
    
    return render(request, {'user': user})




