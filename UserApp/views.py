from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
# rest frame ork and simple jwt
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from UserApp.models import User

from UserApp.serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


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


def check_user(request):
    auth_header = request.headers.get('Authorization', None)

    if not auth_header:
        json_response = {"message": "You are not logged in"}
        return json_response

    try:
        # Parse the token from the Authorization header
        auth_token = auth_header.split(' ')[1]
    except IndexError:
        json_response = {"message": "Authorization header must be in the format 'Bearer <token>'"}
        return json_response

    # Validate the token and get the user
    jwt_authenticator = JWTAuthentication()
    try:
        validated_token = jwt_authenticator.get_validated_token(auth_token)
        user = jwt_authenticator.get_user(validated_token)
        return user
    except (InvalidToken, TokenError, AuthenticationFailed):
        json_response = {"message": "Invalid or expired token"}
        return json_response