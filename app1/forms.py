from django import forms
from .models import stores   # IMPORTANTE: para cargar las tiendas


class newstoreform(forms.Form):
    name = forms.CharField(
        label='Name', max_length=50,
        widget=forms.TextInput(attrs={'class': 'textinp'}))
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea(attrs={'class': 'textinp'}))


class newproductform(forms.Form):
    title = forms.CharField(
        label='Title', max_length=100,
        widget=forms.TextInput(attrs={'class': 'textinp'}))
    
    price = forms.FloatField(
        label='Price',
        widget=forms.NumberInput(attrs={'class': 'textinp'}))
    
    # CAMBIO IMPORTANTE: ahora es SELECT en lugar de TextInput
    store = forms.ModelChoiceField(
        label='Store',
        queryset=stores.objects.all(),
        widget=forms.Select(attrs={'class': 'textinp'})
    )


class newcontactform(forms.Form):
    email = forms.CharField(
        label='Email', max_length=100,
        widget=forms.TextInput(attrs={'class': 'textinp'}))
