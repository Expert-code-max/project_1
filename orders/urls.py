from django.urls import path
from . import views #import all views

urlpatterns = [
    path('', views.order_list, name='order_list'),  # List all orders
    #path('create/', views.create_order, name='create_order'),  # Create a new order
    #path('detail/<int:order_id>/', views.order_detail, name='order_detail'),  # View order details
    #path('edit/<int:order_id>/', views.edit_order, name='edit_order'),  # Edit an existing order
    #path('delete/<int:order_id>/', views.delete_order, name='delete_order'),  # Delete an order
]