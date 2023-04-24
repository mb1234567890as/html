from django import forms  

from .models import *

from django.core.validators import MinValueValidator, MaxValueValidator

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('user_name', 'email', 'password', )

class GenerateRandomUserForm(forms.Form):
    total = forms.IntegerField(
        validators=[
            MinValueValidator(50),
            MaxValueValidator(5000)
        ]
    )
