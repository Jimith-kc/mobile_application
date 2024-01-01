from django import forms
from django.forms import Form
from mobile.models import Mobiles

#for import auth
from django.contrib.auth.models import User

class MobileForm(forms.ModelForm):
    class Meta:
        model=Mobiles
        fields="__all__"

        widgets={
            "name":forms.TextInput(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            "brand":forms.TextInput(attrs={"class":"form-control"}),
            "specs":forms.TextInput(attrs={"class":"form-control"}),
            "display":forms.TextInput(attrs={"class":"form-control"})
            }

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["email","username","password"]

class LoginForm(forms.Form):  #only call Form becouse we only want login no change or update needed
    #so no need of meta model fields
    username=forms.CharField()
    password=forms.CharField()