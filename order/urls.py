from django.urls import path
from . import views

urlpatterns = {
    path('', views.ToOrderView.as_view()),
    path('order.html', views.OrderListView.as_view())
}
