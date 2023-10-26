from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import pre_save
# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__ (self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blogs:artist", kwargs={"pk": self.pk})

class Album(models.Model):
    title = models.CharField(max_length=225)
    date_created = models.DateField()
    author = models.ForeignKey(Artist, on_delete=models.PROTECT, default=False)
    categories = models.ManyToManyField('Category')
    image = models.ImageField(upload_to='albums/', blank=True, null=True)
    
    def __str__ (self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blogs:album", kwargs={"pk": self.pk})
    


class Post(models.Model):
    title = models.CharField(max_length=225)
    date_created = models.DateTimeField(auto_now_add= True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    album = models.ForeignKey(Album, on_delete=models.PROTECT)
    categories = models.ManyToManyField('Category',)
    
    pub_date = models.DateTimeField(default=timezone.now)
    rating = models.IntegerField(default=1, choices=zip(range(1, 6), range(1, 6)))
    lecturas = models.IntegerField(default=1)
    featured = models.FloatField(default=0)
    
    
    def get_absolute_url(self):
        return reverse("blogs:post", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__ (self):
        return self.title
    
    
    def featured_calc(self):
        a = 1  # ponderación cantidad de lecturas
        b = 30  # ponderación cantidad de publicaciones del autor
        c = 50  # ponderación cantidad de días desde que se publicó
        fecha_referencia = timezone.now()
        diferencia_dias = (fecha_referencia - self.pub_date).days
        featured_number = a * self.lecturas + b * self.author.cantidad_publicaciones() - c * diferencia_dias
        return float(featured_number)

    def save(self, *args, **kwargs):
        self.featured = self.featured_calc()  # Calcula 'featured' antes de guardar
        super(Post, self).save(*args, **kwargs)

    # Resto de tu modelo

# Signal para calcular 'featured' antes de guardar el objeto
@receiver(pre_save, sender=Post)
def calculate_featured(sender, instance, **kwargs):
    instance.featured = instance.featured_calc()
    
    
    
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
    


