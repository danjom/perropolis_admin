from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from custom_users.models import *
from webapp.models import *
from django.utils.translation import gettext as _
#from django.core import serializers
import json


class AccessLogForm(forms.ModelForm):
    class Meta:
        model = AccessLogs
        fields = ('user','registrator','client','area',)


class LoginForm(AuthenticationForm):
    '''Simple login form'''
    username = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control form-control-user', 'type': 'email', 'name': 'email', 'placeholder': 'Email'}),
        label='Email')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control form-control-user', 'type': 'password', 'name': 'password',
               'placeholder': 'Password'}),
        label='Password')

    error_messages = {
        'invalid_login': _(
            "Por favor ingrese un email y un password correcto."
        ),
        'inactive': _("Esta cuenta esta inactiva."),
    }

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )
        if user.groups.get().name == 'Clientes':
            raise forms.ValidationError(
                self.error_messages['invalid_login'],
                code='inactive',
            )

    def get_user(self):
        return self.user_cache

    def get_invalid_login_error(self):

        return forms.ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login',
            params={'username': self.username_field.verbose_name},
        )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')
