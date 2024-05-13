from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from .serializers import CartSerializer


class CartView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        try:
            cart = Cart.objects.filter(user=request.user)
            result = CartSerializer(cart, many=True).data
        except Cart.DoesNotExist:
            result = {'message': 'Cart is Empty'}
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        serialized_cart = CartSerializer(context={'request': request}, data=request.data)
        serialized_cart.is_valid(raise_exception=True)
        serialized_cart.save()
        return Response(serialized_cart.data, status=status.HTTP_200_OK)
        
    def delete(self, request):
        try:
           cart = Cart.objects.filter(user=request.user)
           cart.delete()
           result = {'message': 'Cart is emptied successfully'}
        except Cart.DoesNotExist:
            result = {'message': 'Cart is allready empty'}
        return Response(result, status=status.HTTP_200_OK)