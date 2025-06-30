from django.contrib import admin
from . models import Order

# Register your models here.  - make models visible in the admin interface
admin.site.register(Order)
#admin.site.register(Product)
admin.site.site_header = "BuyClick Admin"
admin.site.site_title = "BuyClick Admin Portal"
admin.site.index_title = "Welcome to the BuyClick Admin Portal"#