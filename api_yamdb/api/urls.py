from api.views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitleViewSet, UsersViewSet, authenticatе,
                       signup)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('categories', CategoryViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router.register('users', UsersViewSet, basename='users')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', authenticatе),
]
