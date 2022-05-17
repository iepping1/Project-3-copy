from django.contrib import admin

# import models
# from orders.model.general import BaseModel, Pricing, Topping
# from orders.model.menu import MenuItem, MenuCategory

# # Register your models here.
# # for model in models
# #     admin.site.register(model)
# admin.site.register(BaseModel)
# admin.site.register(Pricing)
# admin.site.register(Topping)
# admin.site.register(MenuItem)
# admin.site.register(MenuCategory)

from .models import *

admin.site.register(Topping)
admin.site.register(PizzaType)
admin.site.register(Pizza)
admin.site.register(SubType)
admin.site.register(Sub)
admin.site.register(SaladType)
admin.site.register(Salad)
admin.site.register(PastaType)
admin.site.register(Pasta)
admin.site.register(PlatterType)
admin.site.register(DinnerPlatter)
admin.site.register(ProperOrder)
