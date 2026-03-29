from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm

from apps.users.models import CustomUser


class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите пароль'
        })


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите имя пользователя',
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите email',
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Введите пароль',
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Повторите пароль',
        })



class EmailForm(PasswordResetForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email не найден")
        return email


class ResetKeyForm(forms.Form):
    reset_key = forms.CharField(
        max_length=6,
        min_length=6,
        label="Код подтверждения",
        widget=forms.TextInput(attrs={'placeholder': '123456', 'class': 'form-control'})
    )

