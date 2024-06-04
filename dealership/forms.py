# # dealership/forms.py

from django import forms
from .models import Profile, Car

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date']

# Create a form to capture the search query
class CarSearchForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)

class CarFilterForm(forms.Form):
    make = forms.ChoiceField(choices=[], required=False)
    model = forms.ChoiceField(choices=[], required=False)
    fuel = forms.ChoiceField(choices=[], required=False)
    gearbox = forms.ChoiceField(choices=[], required=False)
    year = forms.ChoiceField(choices=[], required=False)
    price = forms.ChoiceField(choices=[], required=False)

    def __init__(self, *args, **kwargs):
        super(CarFilterForm, self).__init__(*args, **kwargs)
        self.fields['make'].choices = [('', 'Any')] + [(make, make) for make in Car.objects.values_list('make', flat=True).distinct()]
        self.fields['model'].choices = [('', 'Any')] + [(model, model) for model in Car.objects.values_list('model', flat=True).distinct()]
        self.fields['fuel'].choices = [('', 'Any')] + [(fuel, fuel) for fuel in Car.objects.values_list('fuel', flat=True).distinct()]
        self.fields['gearbox'].choices = [('', 'Any')] + [(gearbox, gearbox) for gearbox in Car.objects.values_list('gearbox', flat=True).distinct()]
        self.fields['year'].choices = [('', 'Any')] + [(year, year) for year in Car.objects.values_list('year', flat=True).distinct()]
        self.fields['price'].choices = [('', 'Any')] + [(price, price) for price in Car.objects.values_list('price', flat=True).distinct()]
