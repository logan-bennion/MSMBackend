from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Shop, ShopHours
from .serializers import ShopSerializer, ShopHoursSerializer

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Shop.objects.all()
        if self.action in ['update', 'partial_update', 'destroy']:
            return queryset.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def hours(self, request, pk=None):
        shop = self.get_object()
        hours = shop.hours.all()
        serializer = ShopHoursSerializer(hours, many=True)
        return Response(serializer.data)