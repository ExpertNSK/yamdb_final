from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, get_token,
                    signup)

v1 = routers.DefaultRouter()
v1.register('users', UserViewSet)
v1.register('genres', GenreViewSet)
v1.register('categories', CategoryViewSet)
v1.register('titles', TitleViewSet)
v1.register(r'titles/(?P<title_id>\d+)/reviews',
            ReviewViewSet, basename='reviews')
v1.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
            r'/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(v1.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', get_token),
]