from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .services.order_service import OrderService
from permissions import IsManager, IsDeliveryCrewOrManager
from rest_framework.throttling import UserRateThrottle


class OrderView(APIView):
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle]
    order_service = OrderService()

    def get(self, request):
        success, result = self.order_service.get_orders(request.user)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        success, result = self.order_service.place_order(request.user)
        if success:
            return Response(result, status=status.HTTP_202_ACCEPTED)
        return Response(result, status=status.HTTP_404_NOT_FOUND)


class OrderDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    order_service = OrderService()

    def get(self, request, order_id):
        success, result = self.order_service.get_order(user=request.user, order_id=order_id)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, order_id):
        success, result = self.order_service.delete_order(order_id=order_id)
        if success:
            return Response(result, status=status.HTTP_200_OK)
        return Response(result, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, order_id):
        success, result = self.order_service.update_order(
            user=request.user, order_id=order_id, json_data=request.data
        )
        if success:
            return Response(result, status=status.HTTP_202_ACCEPTED)
        return Response(result, status=status.HTTP_403_FORBIDDEN)
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            # Apply IsManager permission class only for POST method
            return [IsManager()]
        elif self.request.method == 'PATCH':
            # Apply IsDeliveryCrew permission class only for PATCH method
            return [IsDeliveryCrewOrManager()]
        else:
            # No permission classes for other methods
            return []


        


class OrderSpecificView(APIView):
    authentication_classes = [TokenAuthentication]
    
    def get(self, request, orderId):
        pass

    def put(self, request, orderId):
        pass

    def delete(self, request, orderId):
        pass


