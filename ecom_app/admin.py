from django.contrib import admin

from ecom_app.models import *

class Product_Images(admin.TabularInline):
    model = Product_image

class Additional_Informations(admin.TabularInline):
    model = Aditional_details

class Product_Admin(admin.ModelAdmin):
    inlines = (Product_Images,Additional_Informations)

# Register your models here.
admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Product,Product_Admin)
admin.site.register(Main_Category)
admin.site.register(Sub_Category)
# admin.site.register(Product_image)
# admin.site.register(Aditional_details)
admin.site.register(Section )
