from django.urls import path, include
# from .comment import UserHotelCommentViewSet, HotelCommentViewSet
from .views import TagList,Commentdetail,RetrieveUpdateCommentForReply

# router = routers.DefaultRouter()
# router.register('comments', HotelCommentViewSet, basename="hotel-comment")
# router.register('mycomment', UserHotelCommentViewSet, basename="hotel-mycomment")

urlpatterns = [
    
     path('tag/',TagList.as_view()),
     path('addcomment/',Commentdetail.as_view()),
     path('reply/<int:pk>',RetrieveUpdateCommentForReply.as_view()),
]
