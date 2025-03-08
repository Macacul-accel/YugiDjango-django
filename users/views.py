from .serializers import UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import generics, views
from rest_framework.permissions import AllowAny, IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class LoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)} ,status=200)
        return Response(status=401)
    
class LogoutView(views.APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            request.user.auth_token.delete()
            return Response(status=200)
        except Exception as e:
            return Response({'error': e}, status=500)