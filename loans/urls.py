from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.LoanAppAPI.as_view()),
    path('loanapp', views.LoanAppAPI.as_view()),
    path('status', views.StatusAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
