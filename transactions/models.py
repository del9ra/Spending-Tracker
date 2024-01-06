from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=55)

    def __str__(self):
        return self.title


class MonthlyFinances(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f'Your monthly income is {self.monthly_income:,}$'


class Spending(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=155)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f'Category: {self.category}, Description: {self.description}, {self.amount:,}$, on {self.date}'

    def get_absolute_url(self):
        #  is defined in the model,can be used anywhere in views or templates
        # generate a URL for the view
        return reverse("transaction-update", kwargs={"transaction_id": self.id})
