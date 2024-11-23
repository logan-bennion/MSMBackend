from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk=None):
        product = self.get_object()
        user = request.user
        if product in user.favorites.all():
            user.favorites.remove(product)
            return Response({'status': 'removed from favorites'})
        else:
            user.favorites.add(product)
            return Response({'status': 'added to favorites'})

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        return queryset