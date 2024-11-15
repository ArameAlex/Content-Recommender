from rest_framework import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
from threading import Timer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # from model User
        model = User
        # and these fields
        fields = ['id', 'username', 'email', 'phone', 'password', 'role']
        # and the validators for phone and password
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5},
                        'phone': {'write_only': True, 'min_length': 11, 'max_length': 11}}

    # create a user in database
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
            password=validated_data['password'],
            role=validated_data['role']
                                  )
        # and set the password(Hash)
        user.set_password(validated_data['password'])
        user.save()
        return user


def set_phone_login_active_code_to_none(instance):
    instance.phone_login_active_code = None
    instance.save()


@receiver(post_save, sender=User)
def update_phone_login_active_code_after_save(instance, **kwargs):
    Timer(120, set_phone_login_active_code_to_none, [instance]).start()


def set_forgot_pass_active_code_to_none(instance):
    instance.forgot_pass_active_code = None
    instance.save()


@receiver(post_save, sender=User)
def update_forgot_pass_active_code_after_save(instance, **kwargs):
    Timer(120, set_forgot_pass_active_code_to_none, [instance]).start()
