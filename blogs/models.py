from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    overview = models.TextField(max_length= 80)
    date_created = models.DateTimeField(auto_now_add= True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    categories = models.ManyToManyField('Category')
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    pub_date = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse("blogs:post", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__ (self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=225)
    sluge = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse("blogs:post", kwargs={"slug": self.sluge})
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    content = models.TextField(max_length=1000, help_text="ingrese un comentario")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add= True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    class Meta:
        ordering= ['-post_date']
    
    def __str__(self):
        len_title = 15
        if len(self.content)> len_title:
            return self.content[:len_title]+'...'
        return self.content
    

class Album(models.Model):
    title = models.CharField(max_length=225)
    slug = models.SlugField(unique=True)
    date_created = models.DateTimeField()
    author = models.ManyToManyField('Artist')
    categories = models.ManyToManyField('Category')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

class Artist(models.Model):
    name = models.CharField(max_length=100)
    
    

