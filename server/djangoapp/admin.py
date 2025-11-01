from django.contrib import admin
from .models import CarMake, CarModel

# 🔹 Inline class to show CarModel entries within CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Number of empty forms to show

# 🔹 Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'price_usd')
    list_filter = ('type', 'year', 'car_make')
    search_fields = ('name', 'car_make__name')

# 🔹 Admin class for CarMake with inline CarModel
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # ✅ Only use valid fields
    search_fields = ('name',)

    inlines = [CarModelInline]

# 🔹 Register models with admin site
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
