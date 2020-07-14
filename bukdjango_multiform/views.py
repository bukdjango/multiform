from django import forms
from django.http import HttpResponseBadRequest
from django.utils.functional import cached_property
from django.views.generic import TemplateView


class NewMultiForm(type):

    def __init__(cls, name, bases, clsdict):
        super().__init__(name, bases, clsdict)

        if clsdict.get('multiforms'):
            clsdict.setdefault('multiform_field_name', 'formtype')
            field_name = clsdict.get('multiform_field_name')
            for k, v in clsdict['multiforms'].items():
                clsdict['multiforms'][k]['class'] = type(
                    v['class'].__name__,
                    (v['class'],),
                    {field_name: forms.CharField(
                        widget=forms.HiddenInput(),
                        initial=k,
                    )}
                )


class MultiFormView(TemplateView, metaclass=NewMultiForm):
class MultiFormMixin(metaclass=NewMultiForm):

    multiforms = {}
    multiform_field_name = 'formtype'

    def kwargs_getattr(self, name):
        return f'get_kwargs_{name}'

    @property
    def invalid_handle(self):
        return getattr(
            self, f'handle_invalid_{self.form_name}', None
        )

    @property
    def valid_handle(self):
        return getattr(
            self, f'handle_valid_{self.form_name}', None
        )

    @cached_property
    def form_name(self):
        return self.request.POST.get(
            self.multiform_field_name
        )

    @cached_property
    def form_class(self):
        return self.multiforms.get(
            self.form_name
        )['class']

    @cached_property
    def form_params(self):
        return self.multiforms.get(
            self.form_name
        )

    def get_form_kwargs(self, name, params, **kwargs):
        if attrs := params.get('attrs'):
            for attr in attrs:
                kwargs[attr] = getattr(self, attr)
        if kws := params.get('kwargs'):
            for kw in kws:
                kwargs[kw] = self.kwargs[kw]
        if func := getattr(self, self.kwargs_getattr(name), None):
            kwargs.update(func(**kwargs))
        return kwargs


class MultiFormTemplateView(MultiFormMixin, TemplateView):

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for k, v in self.multiforms.items():
            if not kwargs.get(k):
                ctx[k] = v['class'](
                    **self.get_form_kwargs(
                        name=k, params=v,
                    )
                )
        return ctx

    def post(self, request, *args, **kwargs):

        if not self.form_params:
            return HttpResponseBadRequest()

        form = self.form_class(
            **self.get_form_kwargs(
                name=self.form_name,
                params=self.form_params,
                data=request.POST,
                files=request.FILES,
            )
        )

        if form.is_valid():
            return self.form_valid(form)

        return self.form_invalid(form)

    def post_response(self, form):
        return self.render_to_response(
            context=self.get_context_data(**{
                self.form_name: form,
            })
        )

    def form_valid(self, form):
        if handler := self.valid_handle:
            return handler(form=form)
        return self.post_response(form)

    def form_invalid(self, form):
        if handler := self.invalid_handle:
            return handler(form=form)
        return self.post_response(form)
