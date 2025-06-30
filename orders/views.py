from django.shortcuts import render
from .models import Order
from django.http import Http404

# Create your views here.
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'order_list.html', {'orders': orders})
