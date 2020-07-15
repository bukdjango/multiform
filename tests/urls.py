from django.urls import path

from .views import DecoratorFormTemplateView3, DecoratorFormTemplateView2, DecoratorFormTemplateView, MyMultiFormTemplateView1, MyMultiFormTemplateView2, MyMultiFormTemplateView4


urlpatterns = [
    path('<int:some_kwarg>', MyMultiFormTemplateView1.as_view()),
    path('test', MyMultiFormTemplateView2.as_view()),
    path('view4/<int:some_kwarg>', MyMultiFormTemplateView4.as_view()),
    path('decoratorview/<int:some_kwarg>', DecoratorFormTemplateView.as_view()),
    path('decoratorview2/<int:some_kwarg>', DecoratorFormTemplateView3.as_view())
]
