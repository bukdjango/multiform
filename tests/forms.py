from django import forms


class Form1(forms.Form):
    field1 = forms.CharField(widget=forms.TextInput())
    field2 = forms.CharField(widget=forms.TextInput())

    def __init__(self, request, some_kwarg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request
        self.some_kwarg = some_kwarg

    def clean_field1(self):
        if '1' not in self.cleaned_data['field1']:
            raise forms.ValidationError(
                'Error!'
            )


class Form2(forms.Form):
    field1 = forms.CharField(widget=forms.TextInput())
    field2 = forms.CharField(widget=forms.TextInput())
