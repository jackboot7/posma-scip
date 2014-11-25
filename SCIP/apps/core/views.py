from django.views.generic import View
from django.shortcuts import render_to_response


# Create your views here.

class SimpleStaticView(View):
    def get_template_names(self):
        return ''.join(["_partials/", self.kwargs.get('template_name'), ".html"])

    def get(self, request, *args, **kwargs):
        print self.get_template_names()
        return render_to_response(self.get_template_names())
