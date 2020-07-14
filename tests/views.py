from django.views.generic import TemplateView

from bukdjango_multiform.views import MultiFormView
from .forms import Form1, Form2


class MyMultiFormView(MultiFormView):
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
