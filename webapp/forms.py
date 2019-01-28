from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# extend the inbuilt signup form to include extra fields
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    postcode = forms.CharField(max_length=8, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'postcode', 'password1', 'password2', )
