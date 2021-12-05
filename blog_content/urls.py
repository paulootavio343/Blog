from django.urls import path
from blog_content.views import PostCategory, PostDetail, PostIndex, PostSearch

app_name = 'blog_content'

urlpatterns = [
    path('', PostIndex.as_view(), name='index'),
    path('detalhes/<int:pk>/<str:slug>/', PostDetail.as_view(), name='details'),
    path('categoria/<str:category_slug>/',
         PostCategory.as_view(), name='category'),
    path('pesquisa/', PostSearch.as_view(), name='search'),
]
