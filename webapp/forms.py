from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# extend the inbuilt signup form to include extra fields
class SignUpForm(UserCreationForm):
    postcode = forms.CharField(max_length=8, required=False, widget=forms.TextInput(attrs={'placeholder':'Postcode'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
        'username': forms.TextInput(attrs={'placeholder': 'Username'}),
        'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
        'email': forms.TextInput(attrs={'placeholder': 'Email address'}),
        }
    # extend init method to extend widgets for password fields
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
