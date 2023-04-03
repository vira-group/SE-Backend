from rest_framework import serializers
from .models import Comment
from Account.serializers import PublicUserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['user_info','text','created_at','modified_at','rate']

    def get_user_info(self, obj):
        user = obj.writer
        serialize = PublicUserSerializer(instance=user, context=self.context)
        return serialize.data
