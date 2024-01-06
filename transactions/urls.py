from django.urls import path
from .views import (
    income_create_view,
    transaction_create_view,
    transaction_delete_view,
    transaction_list_view,
    transaction_update_view,
    choose_view,
    history_view,
    analytics_view
)


# app_name = 'transactions'
urlpatterns = [
    path('', transaction_list_view, name='transaction-list'),
    path('history/', history_view, name='history'),
    path('choose/', choose_view, name='choose-view'),
    path('create_income/', income_create_view, name='income-create'),
    path('create/', transaction_create_view, name='transaction-create'),
    path('<int:transaction_id>/update/', transaction_update_view, name='transaction-update'),
    path('<int:transaction_id>/delete/', transaction_delete_view, name='transaction-delete'),
    path('analytics/', analytics_view, name='analytics')
]