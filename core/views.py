from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, Order, OrderItem
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.mixins import LoginRequiredMixin


class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args, **kwargs):
        try:    
            order = Order.objects.get(user=self.request.user ,ordered = False )
            context = {
                'object' : order
            }
            return render(self.request, 'order-summary.html', context)

        except ObjectDoesNotExist:
            messages.error(self.request, "You don not have an active order.")
            return redirect("/")

       
    


class HomeView(ListView):
    model = Item
    paginate_by = 10 
    template_name = "home-page.html"
class ItemView(DetailView):
    model = Item
    template_name = "product-page.html"

def checkout(request):
    return render(request, "checkout-page.html")


@login_required
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


@login_required
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



@login_required
def decrease_item_from_cart(request, slug):
    item =  get_object_or_404(Item, slug = slug)
    order_qs = Order.objects.filter(
            user=request.user,
            ordered = False
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get(
                user=request.user,
                item=item,
                ordered=False
            )
            order_item -= 1
            order_item.save()
            return redirect("core:order", slug=slug)







