# -*- coding: utf-8 -*-


"""
    Views for the accounts module.

    Includes:
        AccountListView
        CreateAccountView
        EditAccountView
        DeleteAccountView
        DetailAccountView

"""
from apps.historial.mixins import HistoryMixin
from django.core.urlresolvers import reverse_lazy

from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView, DeleteView

from braces.views import LoginRequiredMixin, GroupRequiredMixin

from apps.accounts.forms import AccountCreationForm, AccountChangeForm


class AccountListView(LoginRequiredMixin, ListView):
    """ Using the ListView generic view, shows all the users in the system """
    template_name = 'accounts/account_list.html'
    object_name = 'user_list'
    raise_exception = True
    paginate_by = 10

    def get_queryset(self):
        """ Filters out the superuser from the selection """
        try:
            query = self.request.REQUEST.get("search-user")
            return User.objects.filter(username__icontains=query).exclude(is_superuser=True)
        except ValueError:
            return User.objects.filter(is_superuser=False)


class AccountDetailView(LoginRequiredMixin, DetailView):
    """ Using the DetailView generic view to show user detailed information """
    model = User
    template_name = 'accounts/account_detail.html'
    context_object_name = 'user_info'
    raise_exception = True


class AccountCreateView(LoginRequiredMixin, HistoryMixin, GroupRequiredMixin, CreateView):
    model = User
    template_name = 'accounts/account_form.html'
    form_class = AccountCreationForm
    success_url = reverse_lazy('account_list')
    group_required = (u'gerentes')
    raise_exception = True


class AccountUpdateView(LoginRequiredMixin, HistoryMixin, GroupRequiredMixin, UpdateView):
    model = User
    template_name = 'accounts/account_form.html'
    form_class = AccountChangeForm
    success_url = reverse_lazy('account_list')
    group_required = (u'gerentes')
    raise_exception = True


class AccountDeleteView(LoginRequiredMixin, HistoryMixin, GroupRequiredMixin, DeleteView):
    model = User
    template_name = 'accounts/account_confirm_delete.html'
    context_object_name = 'account'
    success_url = reverse_lazy('account_list')
    group_required = (u'gerentes')
    raise_exception = True