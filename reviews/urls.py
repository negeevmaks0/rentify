from django.urls import path, include

from django.views.generic import TemplateView


urlpatterns = [
    path(
        'create/<int:booking_id>/',
        TemplateView.as_view(template_name='reviews/create.html'),
        name='review-create-page'
    ),
]
