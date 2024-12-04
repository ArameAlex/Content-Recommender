from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# rest frame ork and simple jwt
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.forms import ModelForm

from UserApp.models import User

from UserApp.serializers import UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # set my value for token
    @classmethod
    def get_token(cls, user):
        # get the token
        token = super().get_token(user)
        # token gets phone or username
        token['phone'] = user.phone
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # get the password from request but none the username
        credentials = {
            'username': '',
            'password': attrs.get("password")
        }
        # filter the user if the phone was the username(request) value
        # or by the username itself
        user_obj = User.objects.filter(phone=attrs.get("username")).first() or User.objects.filter(
            username=attrs.get("username"),).first()
        # if there was a user set the username(response) to user's username
        if user_obj:
            credentials['username'] = user_obj.username
        # return the username and pass to log in
        return super().validate(credentials)


class MyTokenObtainPairView(TokenObtainPairView):
    # login based on the upper class
    serializer_class = MyTokenObtainPairSerializer


class RegisterViewDRF(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# testing out the logout system
class LogoutView(APIView):
    # if the user was authenticated
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # try to get the refresh token and blacklist it
            token = RefreshToken(request.data.get("refresh_token"))
            token.blacklist()

            return Response({"message": f"Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_status_view(request):
    # Check if user is authenticated
    if request.user.is_authenticated:
        # User is logged in; return their details
        return Response({
            "message": f"Hello, {request.user.username}!",
            "user": {
                "username": request.user.username,
                "phone": getattr(request.user, 'phone', None),
            }
        })
    else:
        # User is not logged in; show login link
        return Response({
            "message": "You are not logged in. Please log in to continue.",
            "login_url": "/api/token/"
        })


class UserStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "message": f"Hello, {request.user.username}!",
            "user": {
                "username": request.user.username,
                "phone": getattr(request.user, 'phone', None),
            }
        })
