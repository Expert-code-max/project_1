from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('edit_cart_item/<int:item_id>/', views.edit_cart_item, name='edit_cart_item'),
    #path('detail/<int:product_id>/', views.product_detail, name='product_detail'),
    #path('create/', views.create_product, name='create_product'),
    #path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
    #path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
]