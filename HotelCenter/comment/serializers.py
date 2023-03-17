from rest_framework import serializers
from .models import Comment
# from Account.serializers.user_serializers import PublicUserSerializer


class Comment_serializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    # def get_user_info(self, obj):
    #     user = obj.writer
    #     serialize = PublicUserSerializer(instance=user, context=self.context)
    #     return serialize.data
