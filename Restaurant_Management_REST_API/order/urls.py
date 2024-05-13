from django.urls import path
from . import views

urlpatterns = [
    path("<int:order_id>", views.OrderDetailView.as_view()),
    path("", views.OrderView.as_view()),
]
