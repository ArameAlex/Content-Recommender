from rest_framework import serializers

from ContentApp.models import PostComment


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        # Model and fields definition
        model = PostComment
        fields = ['message']
