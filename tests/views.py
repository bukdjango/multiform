from django.http import HttpResponse
from django.views.generic import TemplateView

from bukdjango_multiform.views import MultiFormTemplateView
from .forms import Form1, Form2


class MyMultiFormTemplateView1(MultiFormTemplateView):
    template_name = 'index.html'
    multiform_field_name = 'zxc'
    multiforms = {
        'form1_ctx': {
            'class': Form1,
            'attrs': ('request',),
            'kwargs': ('some_kwarg',),
        },
        'form2_ctx': {
            'class': Form2,
        }
    }

    def get_kwargs_form1_ctx(self, **kwargs):
        return {}

    def get_kwargs_form2_ctx(self, **kwargs):
        return {}


class MyMultiFormTemplateView2(MultiFormTemplateView):
    template_name = 'index.html'
    multiforms = {
        'form2_ctx': {
            'class': Form2,
        },
        'form1_ctx': {
            'class': Form1,
        },
    }

    def get_kwargs_form1_ctx(self, **kwargs):
        kwargs.update({
            'request': None,
            'some_kwarg': None,
        })
        return kwargs

    def handle_valid_form2_ctx(self, form):
        return HttpResponse(b'VALID!form2_ctx')

    def handle_invalid_form2_ctx(self, form):
        return HttpResponse(b'INVALID!form2_ctx')

    def handle_valid_form1_ctx(self, form):
        return HttpResponse(b'VALID!form1_ctx')

    def handle_invalid_form1_ctx(self, form):
        return HttpResponse(b'INVALID!form1_ctx')
