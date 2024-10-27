from django import forms

from .models import Vehicle

class VehicleForm(forms.Form):

    name=forms.CharField()

    varient=forms.CharField()

    description=forms.CharField(widget=forms.Textarea)

    fuel_type=forms.ChoiceField(choices=Vehicle.fuel_options)

    running_km=forms.IntegerField()

    color=forms.CharField()

    price=forms.IntegerField()

    brand=forms.CharField()

    owner_type=forms.ChoiceField(choices=Vehicle.owner_options)
