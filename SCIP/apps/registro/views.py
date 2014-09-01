# -*- coding: utf-8 -*-


"""
    Views for the registro module.

    Includes:
        RegistroView

"""

from django.views.generic import TemplateView
from braces.views import LoginRequiredMixin


class RegistroView(LoginRequiredMixin, TemplateView):
    """ Using the ListView generic view, shows all the users in the system """
    template_name = 'horarios/registrar-llegada.html'
    # object_name = 'user_list'
    # raise_exception = True
    # paginate_by = 10

    # def get_queryset(self):
    #     """ Filters out the superuser from the selection """
    #     try:
    #         query = self.request.REQUEST.get("search-user")
    #         return User.objects.filter(username__icontains=query).exclude(is_superuser=True)
    #     except ValueError:
    #         return User.objects.filter(is_superuser=False)

