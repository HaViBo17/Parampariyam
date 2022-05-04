from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
class newTransactionForm(forms.Form):
    type = forms.ChoiceField(
        choices = (
            ('C', "Coin Transaction"), 
            ('F', "File Transaction"),
        ),
        widget = forms.RadioSelect,
        initial = 'coin',
    )
    accounts_to = forms.CharField(
        widget = forms.Textarea(),
        max_length= 10000,
    )


