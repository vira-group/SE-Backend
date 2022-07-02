import rest_framework.request
from rest_framework import permissions
from .models import Comment


class IsWriterOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # only the writer of comment can delete or change it
        return obj.writer == request.user


# class IsWriter(permissions.BasePermission):
#
#     def has_object_permission(self, request, view, obj):
#         # only the writer of comment can delete or change it
#         return obj.writer == request.user
