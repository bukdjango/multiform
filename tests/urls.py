from django.urls import path

from .views import MyMultiFormView


urlpatterns = [path('<int:some_kwarg>', MyMultiFormView.as_view())]
