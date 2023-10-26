from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blogs.models import Post, Category, Album, Artist
from users.models import User
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from blogs.forms import PostCommentForm, ReviewForm
import random
from django.shortcuts import get_object_or_404
# Create your views here.


def home_page(request):
    if request.user.is_authenticated:
        # Obtén los usuarios a los que sigue el usuario actual
        following_users = request.user.following.all()
        
        # Filtra los Post de los usuarios a los que sigues
        posts = Post.objects.filter(
            author__in=following_users,
            pub_date__lte=timezone.now()
        )
    else:
        # Si el usuario no ha iniciado sesión, muestra todos los Post
        posts = Post.objects.filter(pub_date__lte=timezone.now())
    all_albums = Album.objects.all()
    albums = random.sample(list(all_albums), 3)
    context= {
        
        'post_list' : posts,
        'albums' : albums
    }
    
    return render(request, 'blogs/home_page.html', context=context)

def create_post(request):
    albums = Album.objects.all()
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user  # Asigna el autor actual
            
            new_post.save()
            return redirect('blogs:home')  # Redirige a la página deseada después de crear el post
    else:
        form = ReviewForm()
    return render(request, 'blogs/new_post.html', {'form': form, 'album':albums})



class PostDetailView(generic.DetailView):
    model = Post
    queryset = posts = Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['form']= PostCommentForm()
        return context

class PostCommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'blogs/post_detail.html'
    form_class = PostCommentForm
    model = Post
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        f = form.save(commit = False)
        f.author = self.request.user
        f.post = self.object
        f.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('blogs:post', kwargs= {'pk':self.object.pk}) + '#comments-section'
    
class PostView(View):
    def get(s3elf, request,*args,**kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)
    
    def post(s3elf, request,*args,**kwargs):
        view = PostCommentFormView.as_view()
        return view(request,*args,**kwargs)
    
    
class FeaturedListView(generic.ListView):
    moodel = Post
    template_name = 'blogs/results.html'
    
    
    def get_queryset(self):
        query = Post.objects.filter(featured =True).filter(
        pub_date__lte=timezone.now()
    )
        
        return query
    
    
    
class CategoryListView(generic.ListView):
    model = Album
    template_name = "blogs/categories_results.html"

    def get_queryset(self):
        query = self.request.path.replace('/category/','')
        
        album_list = Album.objects.filter(categories__id = query)
        return album_list
    
   
    
class SearchReviewsView(generic.TemplateView):
    template_name = "blogs/results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query) | Q(author__username__icontains=query)
        ).filter(pub_date__lte=timezone.now()).distinct()

        user_list = User.objects.filter(Q(username__icontains=query)).distinct()
        album_list = Album.objects.filter(Q(title__icontains=query)).distinct()
        results = {
            'post_list': post_list,
            'user_list': user_list,
            'album_list':album_list,
            'query':query
        }

        context['results'] = results

        return results
    
    
    
class SearchUsersView(generic.TemplateView):
    template_name = "blogs/user_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query) | Q(author__username__icontains=query)
        ).filter(pub_date__lte=timezone.now()).distinct()

        user_list = User.objects.filter(Q(username__icontains=query)).distinct()
        album_list = Album.objects.filter(Q(title__icontains=query)).distinct()
        results = {
            'post_list': post_list,
            'user_list': user_list,
            'album_list':album_list,
            'query':query
        }

        context['results'] = results

        return results
    
class SearchAlbumsView(generic.TemplateView):
    template_name = "blogs/album_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query) | Q(author__username__icontains=query)
        ).filter(pub_date__lte=timezone.now()).distinct()

        user_list = User.objects.filter(Q(username__icontains=query)).distinct()
        album_list = Album.objects.filter(Q(title__icontains=query)).distinct()
        results = {
            'post_list': post_list,
            'user_list': user_list,
            'album_list':album_list,
            'query':query,
        }

        context['results'] = results

        return results
    

class SearchArtistView(generic.TemplateView):
    template_name = "blogs/artist_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('search')
        
        post_list = Post.objects.filter(
            Q(title__icontains=query) | Q(categories__title__icontains=query) | Q(author__username__icontains=query)
        ).filter(pub_date__lte=timezone.now()).distinct()

        user_list = User.objects.filter(Q(username__icontains=query)).distinct()
        artist_list = Artist.objects.filter(Q(name__icontains=query)).distinct()
        album_list = Album.objects.filter(Q(title__icontains=query)).distinct()
        results = {
            'artist_list': artist_list,
            'post_list': post_list,
            'user_list': user_list,
            'album_list':album_list,
            'query':query,
        }

        context['results'] = results

        return results





    
class AlbumDetailView(generic.DetailView):
    model = Album
    template_name = 'blogs/album_detail.html'
    
    
    
    def get_object(self, queryset=None):
        album_id = self.kwargs.get('pk')  # Obtén el user_id desde los parámetros de la URL
        return get_object_or_404(Album, pk=album_id)


class ArtistDetailView(generic.ListView):
    model = Album
    template_name = 'blogs/artist_detail.html'
    context_object_name = 'album_list'

    def get_queryset(self):
        # Obtén el artista a través de su clave primaria (pk) desde la URL
        artist = Artist.objects.get(pk=self.kwargs['pk'])
        # Filtra los álbumes relacionados con el artista
        return Album.objects.filter(author=artist)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega el artista al contexto
        context['artist'] = Artist.objects.get(pk=self.kwargs['pk'])
        return context