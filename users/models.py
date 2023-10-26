from django.db import models
from django.contrib.auth.models import AbstractUser
from blogs.models import Post
from django.urls import reverse


# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='default.jpg')
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    
    

    def __str__(self):
        return f'{self.username}'
    
    def cantidad_publicaciones(self):
        return Post.objects.filter(author=self).count()
    
    def get_absolute_url(self):
        return reverse("users:profile", kwargs={"user_id": self.id})
    
    def rating(self):
        # Obtén todos los posts del usuario
        user_posts = Post.objects.filter(author=self)
        
        # Inicializa variables para el cálculo del promedio
        total_rating = 0
        total_posts = 0
        
        # Calcula la suma total de los ratings y cuenta los posts
        for post in user_posts:
            total_rating += post.rating
            total_posts += 1
        
        # Evita la división por cero
        if total_posts > 0:
            # Calcula el promedio
            average_rating = total_rating / total_posts
            return average_rating
        else:
            return 0  # Otra valor predeterminado apropiado si el usuario no tiene publicaciones

 