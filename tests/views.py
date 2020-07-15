from django.http import HttpResponse, HttpResponseForbidden

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


class MyMultiFormTemplateView3(MyMultiFormTemplateView1):
    template_name = 'index.html'
    multiforms = {
        'form3_ctx': {
            'class': Form2,
        },
    }


class MyMultiFormTemplateView4(MyMultiFormTemplateView1):
    template_name = 'index.html'
    multiforms = {
        'form4_ctx': {
            'class': Form2,
        },
        'form2_ctx': None,
    }


def logged_in(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseForbidden(b'loginplease')


def thats408(request, *args, **kwargs):
    return HttpResponse(status=408)


def thatsok(request, *args, **kwargs):
    pass


class DecoratorFormTemplateView(MultiFormTemplateView):

    template_name = 'index.html'
    multiforms = {
        'form1_ctx': {
            'class': Form1,
            'attrs': ('request',),
            'kwargs': ('some_kwarg',),
            'checks': (logged_in,)
        }
    }


class DecoratorFormTemplateView2(MultiFormTemplateView):

    template_name = 'index.html'
    multiforms = {
        'form1_ctx': {
            'class': Form1,
            'attrs': ('request',),
            'kwargs': ('some_kwarg',),
            'checks': (thatsok, thats408, logged_in,),
        }
    }


class DecoratorFormTemplateView3(MultiFormTemplateView):

    template_name = 'index.html'
    multiforms = {
        'form1_ctx': {
            'class': Form1,
            'attrs': ('request',),
            'kwargs': ('some_kwarg',),
            'save': True,
        },
        'form2_ctx': {
            'class': Form1,
            'attrs': ('request',),
            'kwargs': ('some_kwarg',),
            'save': True,
        },
        'form3_ctx': {
            'class': Form2,
        },
    }
