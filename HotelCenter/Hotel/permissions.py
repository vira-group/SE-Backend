import rest_framework.request
from rest_framework import permissions
from .models import Room


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow creator of an hotel to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.creator == request.user


class IsEditor(permissions.IsAuthenticated):
    """
    Custom permission to only allow editors or creator of an hotel to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user or request.user in obj.editors


class IsEditorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow editors or creator of an hotel to edit it.
    """

    def has_object_permission(self, request: rest_framework.request.Request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # print('in obj prem ', request.method)
            return True
        # if not bool(request.user.is_authenticated):
        #     return False

        return obj.hotel.creator == request.user or request.user in obj.hotel.editors.all()


class IsRoomSpaceOwnerOrEditor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.room.hotel.creator == request.user or request.user in obj.room.hotel.editors.all()

    def has_permission(self, request, view):
        # print(view.room_id, "preere\n")
        # if request.method in permissions.SAFE_METHODS:
        #     # print('in obj prem ', request.method)
        #     return True

        # room: Room = Room.objects.get(pk=view.room_id)
        try:
            # print('in permission has ', view.room_id)
            room: Room = Room.objects.get(pk=view.room_id)
            # print('room', room)
            if room.hotel.creator == request.user or request.user in room.hotel.editors:
                return True
        except:
            # print('not found per')
            return False

        return True
