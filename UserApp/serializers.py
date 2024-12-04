from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5},
            'phone': {'write_only': True, 'min_length': 11, 'max_length': 11},}
        # }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )
        # Hash the user's password
        user.set_password(validated_data['password'])
        user.save()
        return user
