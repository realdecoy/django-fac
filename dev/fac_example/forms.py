from django import forms

class PaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=20, required=True)
    card_number = forms.CharField(max_length=20, required=True)
    card_cvv = forms.CharField(max_length=4, required=True)
    exp_date = forms.CharField(max_length=5, required=True)
    card_holder_name = forms.CharField(max_length=48, required=True)

    def clean_amount(self):
        return float(self.cleaned_data['amount'])