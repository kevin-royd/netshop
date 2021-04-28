from django.urls import path, re_path
from . import views

urlpatterns = {
    path('', views.IndexView.as_view()),
    re_path('category/(\d+)', views.IndexView.as_view()),
    re_path('category/(\d+)/page/(\d+)', views.IndexView.as_view()),
    re_path('goodsdetails/(\d+)', views.DetailView.as_view()),
}
