from rest_framework import serializers
from .models import Comment



class CommentSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_user_info(self, obj):
        user = obj.writer
        serialize = PublicUserSerializer(instance=user, context=self.context)
        return serialize.data
