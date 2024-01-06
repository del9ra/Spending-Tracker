from .models import Category, Spending, MonthlyFinances
from django import forms


class IncomeForm(forms.ModelForm):
    # model instances names in forms must be exactly same as in models
    monthly_income = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'Enter your monthly income: $',
                                                                        'style': 'width: 250px;'}))

    class Meta:
        model = MonthlyFinances
        fields = ['monthly_income']

    # do not enter a negative number
    def clean_monthly_income(self):
        monthly_income = self.cleaned_data.get('monthly_income')
        if monthly_income < 0:
            raise forms.ValidationError("Monthly income cannot be negative.")
        return monthly_income


class TransactionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Name or Place of making spending: $',
                                                                'style': 'width: 320px'}))
    amount = forms.DecimalField(widget=forms.NumberInput(attrs={'placeholder': 'How much did you spend?',
                                                                'style': 'width: 220px'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%Y-%m-%d'])

    class Meta:
        model = Spending
        fields = ['category', 'description', 'amount', 'date']
