from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('no-you-may-not-ever/', admin.site.urls),
    path('', include('loans.urls'))
]
