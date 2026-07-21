from django.urls import path

from .views import PropertyListPageView, PropertyCreatePageView, PropertyCabinetPageView, PropertyEditPageView

urlpatterns = [
    path('', PropertyListPageView.as_view(), name='properties-page'),
    path('create/', PropertyCreatePageView.as_view(), name='property-create'),
    path('cabinet/', PropertyCabinetPageView.as_view(), name='property_cabinet'),
    path(
        'edit/<int:property_id>/',
        PropertyEditPageView.as_view(),
        name='property-edit'
    ),
]
