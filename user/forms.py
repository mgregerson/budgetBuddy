from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2',)


class CustomUserChangeForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(), label='Current Password')

    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = ('email',)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password and not authenticate(username=self.instance.email, password=password):
            raise forms.ValidationError('Invalid password. Please enter your current password.')
        return password
    
class CustomUserLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Invalid username or password.')
        
        return cleaned_data