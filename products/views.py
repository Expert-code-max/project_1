from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Cart

# Create your views here.

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'products/product_detail.html' , {'product': product})

def view_cart(request):
    cart_items  = Cart.objects.all()
    total_cart_price = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cart_price': total_cart_price})

def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)

        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1
           
        cart_item, created = Cart.objects.get_or_create(product=product)

        if not created:
            cart_item.quantity += quantity
            messages.success(request, f'Quantity for {product.name} updated in cart.')
        else:
            cart_item.quantity = quantity
            messages.success(request, f'{product.name} added to cart.')

        cart_item.save()
        return redirect('view_cart')
    else:
        messages.error(request, "invalid request to add to cart")
        return redirect('product_list')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)
    product_name = cart_item.product.name
    cart_item.delete()
    return redirect('view_cart') 

def edit_cart_item(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity < 1:
                quantity = 1
        except ValueError:
            quantity = 1

        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Cart item updated: {cart_item.product.name}-{cart_item.quantity} pcs.')

        return redirect('view_cart') 

    return render(request, 'edit_cart_item.html', {'cart_item': cart_item})


