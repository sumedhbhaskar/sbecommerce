from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages


class HomeView(ListView):
    model = Item
    template_name = "home-page.html"
class ItemView(DetailView):
    model = Item
    template_name = "product-page.html"

def checkout(request):
    return render(request, "checkout-page.html")

def add_to_cart(request, slug):

    item =  get_object_or_404(Item, slug = slug)
    order_item, created = OrderItem.objects.get_or_create(item=item, user = request.user,ordered = False)
    
    order_qs = Order.objects.filter(user=request.user, ordered = False)
    if order_qs.exists():
        order = order_qs[0]
        # we check ed whether ordered item was in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, " the quantity was modified for this item")
            return redirect("core:product-page", slug=slug)  
        else:
            messages.info(request, " this item was added in your exsiting order ")
            order.items.add(order_item)
            return redirect("core:product-page", slug=slug)      
    else:

        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, 
            ordered_date = ordered_date 
        )
        order.items.add(order_item)
        message.info(request, " this item was added in the empty cart ")
        return redirect("core:product-page", slug=slug)    

def remove_from_cart(request, slug):
        item =  get_object_or_404(Item, slug = slug)

        order_qs = Order.objects.filter(
            user=request.user,
            ordered = False
        )

        if order_qs.exists():
            order = order_qs[0]
            # we check ed whether ordered item was in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item = OrderItem.objects.filter(
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]

                order.items.remove(order_item)
                messages.info(request, " this item was removed from your cart")
                return redirect("core:product-page", slug=slug)

            else:
                messages.info(request, " item not found in the cart")                
                return redirect("core:product-page", slug=slug)

        messages.info(request, "")
        return redirect("core:product-page", slug=slug)     

