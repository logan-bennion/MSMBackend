# apps/cart/views.py
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch
from .models import Cart, CartItem
from .serializers import CartSerializer
import logging

logger = logging.getLogger(__name__)

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        # Optimize query with prefetch_related
        cart, created = Cart.objects.prefetch_related(
            'items',
            'items__product'
        ).get_or_create(id=1)
        return Cart.objects.filter(id=cart.id)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        try:
            logger.debug(f"Add item request data: {request.data}")
            
            # Get cart
            cart, created = Cart.objects.get_or_create(id=1)
            
            # Get data from request
            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))
            
            logger.debug(f"Adding product {product_id} with quantity {quantity} to cart {cart.id}")

            # Get or create cart item
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={'quantity': quantity}
            )

            if not created:
                cart_item.quantity += quantity
                cart_item.save()

            logger.debug(f"Cart item {'created' if created else 'updated'}: {cart_item.id}")

            # Refresh cart from database
            cart.refresh_from_db()
            serializer = self.get_serializer(cart)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error adding item to cart: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        try:
            logger.debug(f"Remove item request data: {request.data}")
            
            # Get cart
            cart = Cart.objects.get(id=1)
            
            # Get product_id from request
            product_id = request.data.get('product_id')
            
            if not product_id:
                return Response(
                    {'error': 'Product ID is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            logger.debug(f"Removing product {product_id} from cart {cart.id}")

            try:
                # Find and delete the cart item
                cart_item = CartItem.objects.get(
                    cart=cart,
                    product_id=product_id
                )
                cart_item.delete()
                logger.debug(f"Successfully removed cart item")

                # Refresh and return updated cart
                cart.refresh_from_db()
                serializer = self.get_serializer(cart)
                return Response(serializer.data)

            except CartItem.DoesNotExist:
                logger.warning(f"Attempted to remove non-existent cart item. Cart: {cart.id}, Product: {product_id}")
                return Response(
                    {'error': 'Item not found in cart'},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Cart.DoesNotExist:
            logger.error("Cart not found")
            return Response(
                {'error': 'Cart not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.error(f"Error removing item from cart: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def list(self, request):
        try:
            logger.debug("Getting cart")
            cart, created = Cart.objects.prefetch_related(
                'items',
                'items__product'
            ).get_or_create(id=1)
            
            serializer = self.get_serializer(cart)
            return Response(serializer.data)
            
        except Exception as e:
            logger.error(f"Error getting cart: {str(e)}", exc_info=True)
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )