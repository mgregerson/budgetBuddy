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
    
class CustomUserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = CustomUser.objects.get(email=email)
                user = authenticate(username=user.email, password=password)
                if user:
                    cleaned_data['user'] = user
                    return cleaned_data
                else:
                    raise forms.ValidationError('Invalid email or password.')
            except CustomUser.DoesNotExist:
                raise forms.ValidationError('Invalid email or password.')

        return cleaned_data