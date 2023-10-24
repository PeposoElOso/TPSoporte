from django.urls import path

from blogs import views



app_name = 'blogs'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('post/<int:pk>', views.PostView.as_view(), name='post'),
    path('featured', views.FeaturedListView.as_view(), name='featured'),
    path('category/<int:id>', views.CategoryListView.as_view(), name='category'),
    path('search/', views.SearchReviewsView.as_view(), name='search'),
    path('search-user/', views.SearchUsersView.as_view(), name='search-user'),
    path('search-album/', views.SearchAlbumsView.as_view(), name='search-album'),
    path('search-artist/', views.SearchArtistView.as_view(), name='search-artist'),
    path('newpost/', views.create_post, name='newpost'),
    path('album/<int:pk>', views.AlbumDetailView.as_view(), name='album'),
    path('artist/<int:pk>', views.ArtistDetailView.as_view(), name='artist'),
    
]