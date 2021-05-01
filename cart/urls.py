from django.urls import path
from . import views

urlpatterns = [
    path('', views.AddCartView.as_view()),
    path('queryAll/', views.QueryAllView.as_view())
]
