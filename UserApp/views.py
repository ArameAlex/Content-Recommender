from rest_framework.decorators import api_view
from rest_framework.response import Response
# rest frame ork and simple jwt
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from UserApp.models import User
from django.utils.crypto import get_random_string

from UserApp.serializers import (UserSerializer, update_forgot_pass_active_code_after_save,
                                 update_phone_login_active_code_after_save)

@api_view(('POST',))
def forgot_password(request):
    # get the phone number from request
    forget_pass_form = request.POST.get("phone")
    # from phone number select the first user
    user: User = User.objects.filter(phone__iexact=forget_pass_form).first()
    # if there wasn't any, error 404
    if user is None:
        response_data = {"message": "There is no User with this phone number"}
        return Response(response_data,  status=404)
    else:
        # if there was we generate a new code (url) for user to enter
        activate_code = get_random_string(10)
        # set the code in user's data
        user.forgot_pass_active_code = activate_code
        user.save()  # set null after 3 min
        update_forgot_pass_active_code_after_save(instance=user)
        # we create a variable to save code data
        active_code = user.forgot_pass_active_code
        # Ensure active_code is not None or empty
        if user.forgot_pass_active_code is not None or "":
            response_data = {
                'Message': f'We send your reset password page({active_code})'
            }

            return Response(response_data,  status=200)
        else:
            # if the active code not found
            response_data = {
                'Message': 'Active code not found for this phone number'
            }
            return Response(response_data,  status=404)


@api_view(('POST',))
def reset_password(request, code):
    # first get the user with the code in url
    user: User = User.objects.filter(forgot_pass_active_code__iexact=code).first()
    # if no user found with this code, the code is wrong
    if user is None:
        response_data = {
            'Message': 'There is No Such User or Email Active Code is incorrect'
        }
        return Response(response_data,  status=404)
    # and if it was, will get the password
    user_new_pass = request.POST.get('password')
    user_new_pass_confirm = request.POST.get('confirm_password')
    # if the pass and confirm wasn't the same
    if user_new_pass != user_new_pass_confirm:
        response_data = {
            'Message': 'Password and Confirm Password do not match'
        }
        return Response(response_data, status=201)
    # if it was set the new password
    user.set_password(user_new_pass)
    # null the code so user can't come back
    user.forgot_pass_active_code = None
    user.save()
    response_data = {
        'Message': 'Password changed Successfully'
    }
    return Response(response_data,  status=201)


@api_view(('POST',))
def phone_login(request):
    # get the phone number from request
    phone_login_form = request.POST.get('phone')
    # check if there is user or not based on phone
    user: User = User.objects.filter(phone__iexact=phone_login_form).first()
    # if there was no user, error 404
    if user is None:
        response_data = {
            'Message': f'There is no user with This phone number',
        }
        return Response(response_data,  status=400)
    else:
        # if there was, then try to get the code
        code_form = request.POST.get('code', None)
        # if there wasn't code
        if code_form is None or "":
            # create the code and save it in user data
            activate_code = get_random_string(10)
            user.phone_login_active_code = activate_code
            user.save()
            # set the code none after 3min
            update_phone_login_active_code_after_save(instance=user)
            response_data = {"message": f"code is ({user.phone_login_active_code})"}
            return Response(response_data,  status=200)
        else:
            # check if code is right and not none or not if there was code
            if user.phone_login_active_code == code_form and code_form != "" or None:
                # set the user's code to none
                user.phone_login_active_code = None
                user.save()
                # generate a RefreshToken for the user to login
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'User login was successfully done',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },  status=200)
            else:
                response_data = {"message": "Code Was not correct"}
                return Response(response_data,  status=200)


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


class RegisterViewDRF(APIView):
    def post(self, request):
        # uses serializer and check the user to make it
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# testing out the logout system
class LogoutView(APIView):
    # if the user was authenticated
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            # try to get the refresh token and blacklist it
            token = RefreshToken(request.data.get("refresh_token"))
            token.blacklist()

            return Response({"message": f"Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
