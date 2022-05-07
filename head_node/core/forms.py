from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class newTransactionForm(forms.Form):
    transaction_type = forms.ChoiceField(
        choices = (
            ('C', "Coin Transaction"), 
            ('F', "File Transaction"),
        ),
        widget = forms.RadioSelect,
        initial = 'C',
    )
    # accounts_to = forms.CharField(
    #     widget = forms.Textarea(),
    #     max_length= 10000,
    # )
    account_to = forms.CharField(max_length=1000)
    transaction_data = forms.CharField(max_length=1000)
    transaction_fees = forms.IntegerField(initial=0)

