from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserSerializer
from django.shortcuts import get_object_or_404
from permissions import IsManager
from rest_framework.throttling import UserRateThrottle


class ManagerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManager]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        managers = User.objects.filter(groups__name='Manager')
        serialized_managers = UserSerializer(managers, many=True)
        return Response(serialized_managers.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data.get('username')
        manager_group = Group.objects.get(name='Manager')
        user = get_object_or_404(User, username=username)
        user.groups.add(manager_group)
        return Response({'message': 'User successfully added to Manager group'}, status=status.HTTP_201_CREATED)

class DeliveryCrewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManager]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        delivery_crew = User.objects.filter(groups__name='Delivery Crew')
        serialized_delivery_crew = UserSerializer(delivery_crew, many=True)
        return Response(serialized_delivery_crew.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        username = request.data.get('username')
        delivery_crew_group = Group.objects.get(name='Delivery Crew')
        user = get_object_or_404(User, username=username)
        user.groups.add(delivery_crew_group)
        return Response({'message': 'User succssfully added to Delivery Crew group'}, status=status.HTTP_201_CREATED)


class DeleteManagerView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManager]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, userId):
        user = get_object_or_404(User, username=userId)
        manager_group = Group.objects.get(name='Manager')
        user.groups.remove(manager_group)
        return Response({"message": "User successfully removed from the Manager group"}, status=status.HTTP_200_OK)


class DeleteDeliveryCrewView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsManager]
    throttle_classes = [UserRateThrottle]

    def delete(self, request, userId):
        user = get_object_or_404(User, username=userId)
        delivery_crew_group = Group.objects.get(name='Delivery Crew')
        user.groups.remove(delivery_crew_group)
        return Response({"message": "User successfully removed from the Delivery Crew group"}, status=status.HTTP_200_OK)



