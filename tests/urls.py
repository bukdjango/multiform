from django.urls import path

from .views import MyMultiFormTemplateView1, MyMultiFormTemplateView2


urlpatterns = [
    path('<int:some_kwarg>', MyMultiFormTemplateView1.as_view()),
    path('test', MyMultiFormTemplateView2.as_view()),
]
