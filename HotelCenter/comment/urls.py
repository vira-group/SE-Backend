from django.urls import path, include
from .views import TagList,Commentdetail,RetrieveUpdateCommentForReply,GetAllManagerComments,GetAllHotelComments


urlpatterns = [
    
     path('tag/',TagList.as_view()),
     path('addcomment/',Commentdetail.as_view()),
     path('reply/<int:pk>',RetrieveUpdateCommentForReply.as_view()),
     path('getallmanagercomments/',GetAllManagerComments.as_view()),
     path('getallhotelcomments/<int:pk>',GetAllHotelComments.as_view()),
]
