# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

# Initialize permissions
from rest_framework.permissions import IsAuthenticated

from HotelCenter.permissions import IsManager, IsCustomer

# Permissions for the views
from rest_framework.decorators import permission_classes

@permission_classes([IsAuthenticated , IsCustomer])
def index(request):
    return render(request, 'chat/index.html', {})


@permission_classes([IsAuthenticated , IsManager])
def room(request, room_name):
    return render(request, 'chat/room.html', {
       'room_name': mark_safe(json.dumps(room_name)),
        'id': mark_safe(json.dumps(request.user.id)),
    })