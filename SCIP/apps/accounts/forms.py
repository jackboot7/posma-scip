# -*- coding: utf-8 -*-

"""
    Forms for the accounts module:

    We use crispy_forms to extend and style forms programmatically.
    Checkout http://django-crispy-forms.readthedocs.org/en/ for documentation.

    This module includes:

        LoginForm
        PasswordChangeForm
        PasswordResetForm
        AccountCreationForm
"""

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm


from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import  Submit


bootstrap_helper_attr = (True, True)


class LoginForm(AuthenticationForm):
    """ Django's authentication form extended with crispy helpers"""

    def __init__(self, *args, **kwargs):
        # self.helper = FormHelper()
        # self.helper.form_id = 'id-login-form'
        #
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'login'
        #
        # #Boostrap Helper Attributes
        # self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr
        #
        # self.helper.add_input(Submit('submit', 'Iniciar sesión'))

        super(LoginForm, self).__init__(*args, **kwargs)


class PasswordChangeForm(DjangoPasswordChangeForm):
    """ Django's password change form extended with crispy helpers"""

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id-change-password-form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'password_change'

        # Boostrap Helper Attributes
        self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr

        self.helper.add_input(Submit('submit', 'Enviar'))
        super(PasswordChangeForm, self).__init__(*args, **kwargs)


class AccountCreationForm(UserCreationForm):
    """ Django's user creation form extended with crispy helpers """

    def __init__(self, *args, **kwargs):
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['groups'].label = 'Grupos (Seleccionar uno o mas grupos)'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple()
        }
    
    def save(self, commit=True):
        # will always commit True
        user = super(AccountCreationForm, self).save()
        for group in self.cleaned_data['groups']:
            user.groups.add(group)
                
        user.save()
        return user


class AccountChangeForm(forms.ModelForm):
    """ Django's user update form extended with crispy helpers """

    def __init__(self, *args, **kwargs):
        super(AccountChangeForm, self).__init__(*args, **kwargs)
        if 'initial' in kwargs:
            self.fields['groups'].label = 'Grupos (Seleccionar uno o mas grupos)'

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',  'email', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple()
        }

        # def __init__(self, *args, **kwargs):
        #     self.helper = FormHelper()
        #     self.helper.form_id = 'id-user-change-form'
        #     self.helper.form_method = 'post'
        #
        #     # Boostrap Helper Attributes
        #     self.helper.html5_required, self.helper.help_text_inline = bootstrap_helper_attr
        #
        #     self.helper.add_input(Submit('submit', 'Enviar'))
        #     super(AccountChangeForm, self).__init__(*args, **kwargs)
