from .serializers import PropertySerializer, PropertyImageSerializer
from .models import Property, PropertyImage

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsLandlord, IsOwnerOrReadOnly, IsPropertyOwner

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django.views.generic import TemplateView

from .filters import PropertyFilter

from rest_framework.parsers import MultiPartParser, FormParser



# Create your views here.


class PropertyCreatePageView(TemplateView):
    template_name = 'properties/create.html'



class PropertyListPageView(TemplateView):
    template_name = 'properties/list.html'



class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    filterset_class = PropertyFilter


    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        property = self.get_object()

        if property.owner != request.user:
            return Response(
                {"detail": "You can upload images only to your own properties."},
                status=403
            )

        images = request.FILES.getlist('images')

        if not images:
            return Response(
                {"detail": "No images uploaded."},
                status=400
            )

        created = []

        for image in images:
            obj = PropertyImage.objects.create(property=property, image=image)

            created.append(
                PropertyImageSerializer(
                    obj,
                    context={"request":request}
                ).data
            )


        return Response(created)


    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        property = self.get_object()

        property.is_active = not property.is_active
        property.save()

        return Response({'is_active': property.is_active})


    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated:
            if user.role == 'landlord':
                return Property.objects.filter(owner=user)

        return Property.objects.filter(is_active=True)


    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsLandlord]

        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

        else:
            permission_classes = [AllowAny]


        return [permission() for permission in permission_classes]


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter
    )

    search_fields = (
        'title',
        'description',
        'location'
    )

    ordering_fields = (
        'price_per_month',
        'created_at'
    )



class PropertyImageViewSet(viewsets.ModelViewSet):
    serializer_class = PropertyImageSerializer


    def get_queryset(self):
        return PropertyImage.objects.all()


    def get_permissions(self):
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsPropertyOwner]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]