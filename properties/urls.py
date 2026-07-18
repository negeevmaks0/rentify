from django.urls import path
from .views import PropertyListPageView

urlpatterns = [
    path('', PropertyListPageView.as_view(), name='properties-page'),
]
