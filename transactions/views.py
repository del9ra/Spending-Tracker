from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect
from .models import Spending, Category, MonthlyFinances
from .forms import TransactionForm, IncomeForm
from datetime import datetime, date
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


@login_required
def transaction_list_view(request):
    # filter(customer=request.user) gets access only to current user's data
    queryset = Spending.objects.filter(customer=request.user).order_by('date')[:5]      # limit by 5
    monthly_finances = MonthlyFinances.objects.filter(user=request.user).first()
    # we need 'if' because None is not an object in MonthsFinances model
    income = monthly_finances.monthly_income if monthly_finances else 0
    current_date = date.today()
    # displays spendings in current month
    month = datetime.now().month
    # we needed before '0', as it tried to apply f-string to None, so it caused error
    # don't use 'if' here, as 'aggregate' returns a dict, and None is a valid value for a dictionary key
    # aggregate() is used for operations on the entire data set
    this_month_total_spent = Spending.objects.filter(customer=request.user, date__month=month).aggregate(total_spent=Sum('amount'))['total_spent']
    if this_month_total_spent is None:
        this_month_total_spent = 0
    # category is a foreign key
    # it groups Spending objects by category and calculate the sum of the amount for each group
    # annotate() is used for operations on groups within the data
    expenses_by_category = Spending.objects.filter(customer=request.user, date__month=month).values('category__title').annotate(total_amount=Sum('amount'))
    if income:
        leftover = income - this_month_total_spent
    else:
        leftover = 0
    context = {'object_list': queryset, 'expenses': expenses_by_category, 'total_spent': this_month_total_spent,
               'income': income, 'leftover': leftover, 'date': current_date}
    return render(request, 'transactions/transaction_list.html', context)


@login_required
def analytics_view(request):
    data = []       # list of dicts to pass months to js
    # gets the first MonthlyFinances object for the currently logged-in user
    monthly_finances = MonthlyFinances.objects.filter(user=request.user).first()
    income = monthly_finances.monthly_income if monthly_finances else 0
    all_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

    for month in range(len(all_months)+1):
        # because you have 'customer' field in your Spending model
        spending = Spending.objects.filter(customer=request.user, date__month=month).aggregate(total_spent=Sum('amount'))['total_spent']
        if spending is None:    # spending = spending or 0
            spending = 0
        else:
            leftover = income - spending
            month_name = all_months[month - 1]      # access a month with list index
            month_info = {'month': month_name, 'spent': spending, 'left': leftover}
            data.append(month_info)
    context = {'data': data}
    return render(request, 'transactions/analytics.html', context)


@login_required
def choose_view(request):
    if MonthlyFinances.objects.filter(user=request.user).first() is None:
        # If no object exists, redirect to the income creation page
        return redirect('income-create')
    else:
        # If an object exists, redirect to the transaction creation page
        return redirect('transaction-create')


@login_required
def income_create_view(request):
    # request.POST or None creates a form instance that is either populated with
    # submitted data (if available) or empty (if no data was submitted)
    form = IncomeForm(request.POST or None)
    if form.is_valid():
        # this is how income is associated with the currently logged-in user
        # you need to specify which user the income belongs to
        form.instance.user = request.user
        form.save()
        return redirect('transaction-create')
    context = {'form': form}
    return render(request, 'transactions/income_create.html', context)


@login_required
def transaction_create_view(request):
    form = TransactionForm(request.POST or None)
    if form.is_valid():
        form.instance.customer = request.user
        form.save()
        return redirect('transaction-list')
    # form = TransactionForm() - создает новую пустую форму после сохранения старой
    context = {'form': form}
    return render(request, 'transactions/transaction_create.html', context)


@login_required
def transaction_update_view(request, transaction_id):
    # transaction_id is the ID of the Spending object to be updated.
    # gets the Spending object from DB with id and customer or raises 404 error, if the object is not found
    obj = get_object_or_404(Spending, id=transaction_id, customer=request.user)
    # create a form instance. If the request method is POST, it populates the form with the submitted data.
    # If not, it populates the form with the data from the Spending object 'obj'.
    form = TransactionForm(request.POST or None, instance=obj)
    if form.is_valid():
        # sets the customer attribute of the Spending object to the current user
        form.instance.customer = request.user
        form.save()
        return redirect('transaction-list')
    context = {'form': form}
    return render(request, 'transactions/transaction_create.html', context)


@login_required
def history_view(request):
    # queryset is the data to be paginated; desc order from later to earlier date
    queryset = Spending.objects.filter(customer=request.user).order_by('-date')
    # queryset = Spending.objects.all().order_by('-date')
    paginated = Paginator(queryset, 12)      # initializes paginator
    page_number = request.GET.get('page')  # Get the requested page number from the URL(http://127.0.0.1:8000/?page=2)
    page = paginated.get_page(page_number)  # retrieves the specific page to render from the paginated variable
    context = {'page': page}
    return render(request, 'transactions/history.html', context)


@login_required
def transaction_delete_view(request, transaction_id):
    # customer=request.user - user can only delete their own transactions
    obj = get_object_or_404(Spending, id=transaction_id, customer=request.user)
    if request.method == 'POST':
        obj.delete()        # confirming delete
        return redirect('transaction-list')

    context = {'object': obj}
    return render(request, 'transactions/transaction_delete.html', context)
