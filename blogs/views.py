from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from blogs.models import Post, Category, Album
from django.views import generic, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from blogs.forms import PostCommentForm, ReviewForm

# Create your views here.


def home_page(request):
    posts = Post.objects.filter(
        pub_date__lte=timezone.now()
    )
    categories = Category.objects.all()
    albums = Album.objects.all()[:3]
    context= {
        
        'post_list' : posts,
        
        'albums' : albums
    }
    
    return render(request, 'blogs/home_page.html', context=context)

def create_post(request):
    albums = Album.objects.all()
    print(albums)
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
        print(album_list)
        return album_list
    
   
    
class SearchResultsView(generic.ListView):
    model = Post
    template_name = "blogs/results.html"

    def get_queryset(self):
        query = self.request.GET.get('search')
        post_list = Post.objects.filter(
            Q(title__icontains=query)| Q(categories__title__icontains=query)
            ).filter(
            pub_date__lte=timezone.now()
        ).distinct()
        return post_list
    
    
    
