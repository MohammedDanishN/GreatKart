from django import forms
from .models import Account


class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password',
               'class': 'form-control'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password',]

    def __init__(self, *args, **kwargs):
        super(RegisterationForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            self.fields[i].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Password Doesn't Match")
