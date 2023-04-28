from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                       UserViewSet, ReviewViewSet, CommentViewSet, APISignUp,
                       APITokenView)

app_name = 'api'

router = DefaultRouter()
router.register('users', UserViewSet, basename='users'),
router.register('genres', GenreViewSet, basename='genres')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', APISignUp.as_view(), name='signup'),
    path('v1/auth/token/', APITokenView.as_view(), name='get_token'),
]
