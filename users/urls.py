from django.urls import path
from users import views
from django.views.generic import TemplateView


app_name = 'users'

urlpatterns = [
    path('registration/', views.UserRegistration.as_view(), name = 'registration'),
    path('success/', TemplateView.as_view(template_name= 'users/success_registration.html'), name = 'success'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='profile'),
    path('profile/users/seguir-usuario/<int:user_id>/', views.seguir_usuario, name='seguir-usuario'),

]
    

    
    
