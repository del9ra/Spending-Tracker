# Generated by Django 4.2.6 on 2023-11-15 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_monthlyfinances_remove_spending_income'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MonthlyFinances',
        ),
    ]
