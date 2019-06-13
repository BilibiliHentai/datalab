from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput({'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput({'placeholder': 'Password'}))


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'})
        }

class UploadExcelForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField(widget=forms.FileInput({'class': 'fileipt'}))