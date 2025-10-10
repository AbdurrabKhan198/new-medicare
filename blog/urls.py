from django.urls import path
from . import views

urlpatterns = [
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('search/', views.BlogSearchView.as_view(), name='blog_search'),
    path('category/<slug:slug>/', views.BlogCategoryView.as_view(), name='blog_category'),
    path('tag/<slug:slug>/', views.BlogTagView.as_view(), name='blog_tag'),
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
]
