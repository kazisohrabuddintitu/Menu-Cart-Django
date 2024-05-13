from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle


class RegisterUser(APIView):
    throttle_classes = [UserRateThrottle]

    def post(self, request):
        user = UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response(user.data, status=status.HTTP_201_CREATED)

class ShowUser(APIView):
    authentication_classes = [TokenAuthentication]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        user = UserSerializer(request.user)
        return Response(user.data, status=status.HTTP_200_OK)
