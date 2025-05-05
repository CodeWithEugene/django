from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, FarmerProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.phone_number = self.cleaned_data['phone_number']
        
        if commit:
            user.save()
        return user


class FarmerProfileForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ('farm_name', 'farm_size_acres', 'farm_location', 'farm_description')
        widgets = {
            'farm_description': forms.Textarea(attrs={'rows': 4}),
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = FarmerProfile
        fields = ('farm_name', 'farm_size_acres', 'farm_location', 'farm_description', 'profile_image')