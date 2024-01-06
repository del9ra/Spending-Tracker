from django.contrib import admin
from .models import Category, Spending, MonthlyFinances

# Register your models here.
admin.site.register(Category)
admin.site.register(Spending)
admin.site.register(MonthlyFinances)


