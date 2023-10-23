from django.db import models
from django.contrib.auth.models import AbstractUser
from blogs.models import Post


# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True,default='default.jpg')
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="following")

    def __str__(self):
        return f'{self.username}'
    
    def cantidad_publicaciones(self):
        return Post.objects.filter(author=self).count()
    
 