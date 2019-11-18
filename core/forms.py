from django import forms
from django_countries.fields import CountryField

PAYMENT_OPTION= (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'1234 Main St'
    }))
    shipping_address2 = forms.CharField(required=False,widget=forms.TextInput(attrs={
        'placeholder':'apt or street'
    }) )
    country = CountryField(blank_label='(select country)').formfield()
    zip_code = forms.CharField()
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput())
    save_info = forms.BooleanField(widget=forms.CheckboxInput())
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_OPTION)



