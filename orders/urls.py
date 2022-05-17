from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    # path("add_user", views.add_user, name="add_user"),
    path("register", views.register, name="register"),
    # path("add_item", views.add_item, name='add_item'),
#     path("create_pizza", views.create_pizza, name='create_pizza'),
#     path("create_sub", views.create_sub, name='create_sub'),
#     path("add_pizza", views.add_pizza, name='add_pizza'),
#     path("add_sub", views.add_sub, name='add_sub'),
#     path("cart", views.cart, name='cart'),
#     path("place_order", views.place_order, name='place_order'),
#     path("all_orders", views.all_orders, name='all_orders'),
#     path("order", views.order, name='order'),
#     path("complete_order", views.complete_order, name='complete_order'),
#     path("orders", views.orders, name='orders')
]
