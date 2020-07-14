from django.urls import path

from .views import MyMultiFormView1, MyMultiFormView2


urlpatterns = [
    path('<int:some_kwarg>', MyMultiFormView1.as_view()),
    path('test', MyMultiFormView2.as_view()),
]
