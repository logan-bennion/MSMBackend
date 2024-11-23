from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Wishlist, WishlistItem
from .serializers import WishlistSerializer, WishlistItemSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def toggle_item(self, request):
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')

        try:
            wishlist_item = WishlistItem.objects.get(
                wishlist=wishlist,
                product_id=product_id
            )
            wishlist_item.delete()
            return Response({'status': 'removed from wishlist'})
        except WishlistItem.DoesNotExist:
            WishlistItem.objects.create(
                wishlist=wishlist,
                product_id=product_id
            )
            return Response({'status': 'added to wishlist'})