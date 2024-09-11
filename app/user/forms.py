from django import forms
from django.contrib.auth import get_user_model
from core.models import Person
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


class PersonRegistrationForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'username', 'email', 'date_of_birth', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class PersonLoginForm(forms.Form):

    username = forms.CharField(max_length=30)
    password = forms.CharField(
        widget=forms.PasswordInput,
        strip=False, 
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            person = authenticate(username=username, password=password)
            if person is None:
                raise ValidationError(
                    _('Unable to authenticate with provided credentials.'),
                    code='authorization'
                )
        return cleaned_data


    def login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        person = authenticate(request, username=username, password=password)
        if person is not None:
            login(request, person)
            return True
        return False
    

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254)

class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput,
        strip=False,
    )

    def save(self, commit=True):

        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user