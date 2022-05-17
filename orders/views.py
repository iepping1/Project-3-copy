
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
# from orders.model.menu import MenuItem, MenuCategory
# from orders.model.general import Pricing, Topping


# Create your views here.
def index(request):
    context = {
      "user": request.user,
    #   "regular_pizzas": RegularPizza.objects.all(),
    #   "sicilian_pizzas": SicilianPizza.objects.all(),
    #   "toppings": Topping.objects.all(),
    #   "subs": Subs.objects.all(),
    #   "pastas": Pasta.objects.all(),
    #   "salads": Salads.objects.all(),
    #   "dinner_platters": DinnerPlatters.objects.all()
    }
    return render(request, "user.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "login.html", {"message": "Invalid credentials."})


def logout_view(request):
    # redirect user to login when logged out
    logout(request)
    return render(request, "login.html", {"message": "Logged out."})


def register(request):
    return render(request, "register.html")


def add_user(request):
    #try:
    password = request.POST['password']
    user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
    user.first_name = request.POST['first_name']
    user.last_name = request.POST['last_name']
    user.save()
    # except:
    #     return apology("something must have gone wrong")
    return render(request, 'login.html', {'message': 'Registration complete'})


def create_pizza(request):
    context = {
        'type': request.POST['type'],
        'size': request.POST['size'],
        'price': float(request.POST['price']), 
        'name': request.POST['name'],
        'topping_count': int(request.POST['topping_count'])
    }

    if request.POST['is_special'] == 'True':
        return render(request, 'special.html', context)
    elif request.POST['topping_count'] == '0':
        #add cheese pizza to cart
        text = f"{request.POST['type']} {request.POST['size']} cheese pizza"
        item = CartItem(user=request.user, text=text, price=request.POST['price'])
        item.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        #let user select toppings
        context['toppings'] = Topping.objects.all()
        return render(request, 'toppings.html', context)


def add_pizza(request):
    if request.POST['is_special'] == 'True':
        #add special pizza to cart
        text = f"{request.POST['size']} {request.POST['type']} special pizza: {request.POST['description']}"
        item = CartItem(user=request.user, text=text, price=request.POST['price'])
        item.save()
    else:
        #add pizza with toppings to cart
        toppings = []
        for topping in Topping.objects.all():
            if topping.name in request.POST:
                toppings.append(topping.name)
        text = f"{request.POST['size']} {request.POST['type']} {request.POST['name']} pizza with"
        for topping in toppings:
            text += ' ' + topping + ','
        #remove comma from the end
        text = text[:len(text) - 1]

    item = CartItem(user=request.user, text=text, price=request.POST['price'])
    item.save()
    return HttpResponseRedirect(reverse("index"))


def create_sub(request):
    context = {
        'price': request.POST['price'],
        'name': request.POST['name'],
        'size': request.POST['size'],
        'additions': Subs.objects.get(name=request.POST['name']).possible_additions.all()
    }
    return render(request, 'subs.html', context)


def add_sub(request):
    additions=[]
    for addition in Subs.objects.get(name=request.POST['name']).possible_additions.all():
        if addition.name in request.POST:
            additions.append(addition.name)
    text = f"{request.POST['size']} {request.POST['name']} sub"
    if len(additions) > 0:
        text += ' with'
        for addition in additions:
            text += ' ' + addition + ','
        text = text[:len(text) - 1]
    item = CartItem(user=request.user, text=text, price=request.POST['price'])
    item.save()
    return HttpResponseRedirect(reverse("index"))


def add_item(request):
    if 'size' in request.POST:
        text = f"{request.POST['size']} {request.POST['name']} {request.POST['type']}"
    else:
        text = f"{request.POST['name']} {request.POST['type']}"
    item = CartItem(user=request.user, text=text, price=request.POST['price'])
    item.save()
    return HttpResponseRedirect(reverse("index"))


def cart(request):
    if request.method == 'POST':
        CartItem.objects.get(pk=request.POST['id']).delete()

    items = request.user.cart.all()

    total = 0
    for item in items:
        total += item.price
    context = {
        'items': items,
        'total': total,
        'quantity': len(items)
    }
    return render(request, 'orders/cart.html', context)


def place_order(request):
    order = Order(user=request.user, status=False, total=request.POST['total'], items_count=request.POST['quantity'])
    order.save()
    for item in request.user.cart.all():
        item.order = order
        item.user = None
        item.save()
    context = {
        'message': 'Order placed'
    }
    return HttpResponseRedirect(reverse("index"))


def history(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return render(request, 'orders/error.html', {'error': 'You must be logged in as an administrator to enter this page!'})

    orders = Order.objects.all()
    items = []
    for order in orders:
        items.append(order.items.all())
    context = {
        'orders': orders,
        'items': items
    }
    return render(request, 'history.html', context)


def order(request):
    admin = True
    if not request.user.is_authenticated or not request.user.is_staff:
        admin = False

    order = Order.objects.get(pk=request.POST['id'])
    context = {
        'order': order,
        'items': order.items.all(),
        'admin': admin
    }
    return render(request, 'order.html', context)


def complete_order(request):
    order = Order.objects.get(pk=request.POST['id'])
    order.status = True
    order.save()
    context = {
        'order': order,
        'items': order.items.all()
    }
    return render(request, 'order.html', context)


def orders(request):
    context = {
        'orders': Order.objects.filter(user=request.user),
    }
    return render(request, 'orders.html', context)


