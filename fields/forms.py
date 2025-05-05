from django import forms
from .models import Field, Crop, SoilData
from datetime import date, timedelta

class FieldForm(forms.ModelForm):
    class Meta:
        model = Field
        fields = ['name', 'description', 'size_acres', 'address', 'soil_type', 'latitude', 'longitude', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
        }

class CropForm(forms.ModelForm):
    expected_harvest_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today() + timedelta(days=90)
    )
    planting_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today()
    )
    
    class Meta:
        model = Crop
        fields = ['name', 'variety', 'planting_date', 'expected_harvest_date', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class SoilDataForm(forms.ModelForm):
    reading_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial=date.today()
    )
    
    class Meta:
        model = SoilData
        fields = ['reading_date', 'moisture_percentage', 'temperature', 'ph_level', 'nitrogen', 'phosphorus', 'potassium', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }