from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, CategoryListView, subscribe, IndexView
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('',cache_page(60*1)(NewsList.as_view()),name='news_list'),
   path('<int:pk>',PostDetail.as_view(),name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('article/create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('hello/', IndexView.as_view()),
]
