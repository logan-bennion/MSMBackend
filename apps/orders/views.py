from rest_framework import viewsets, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    #permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        cart_items = request.data.get('cart_items', [])
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_amount=request.data.get('total_amount'),
            shipping_address=request.data.get('shipping_address')
        )

        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear user's cart
        request.user.cart.clear()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)