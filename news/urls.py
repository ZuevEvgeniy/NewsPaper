from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch, CategoryListView, subscribe


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', NewsList.as_view(),name='news_list'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(),name='post_detail'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('article/create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('article/<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
