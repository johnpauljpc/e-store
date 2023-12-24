from django import forms

from .utils.choices import NIGERIA_STATES, PAYMENT_OPTION


class CheckoutForm(forms.Form): 
    shipping_zip = forms.CharField(required= True, widget=forms.TextInput(attrs={
        'placeholder':'Zip code',
        'id':'shipping_zip',  'class':'form-control'
    }))

    state = forms.ChoiceField(choices=NIGERIA_STATES, widget=forms.Select(attrs={
        'class':'form-control'
    }))
     
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'12 Main Street, Nsukka',
        'id':'shipping_address',  'class':'form-control'
    }))

    phone_number = forms.CharField(required=False,max_length=15, widget=forms.TextInput(attrs={
        'type':'tel' ,'placeholder':'+234 8109137270', 'id':'phone_number', 'class':'form-control',
    }))


    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_OPTION)
