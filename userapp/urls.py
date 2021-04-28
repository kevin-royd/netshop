from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('checkUname/', views.checkUnameView.as_view()),
    path('center/', views.CenterView.as_view())
]
