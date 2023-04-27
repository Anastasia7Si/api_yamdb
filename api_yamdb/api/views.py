from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Genre, Title, User
from api.filters import TitleFilter

from api.permissions import (IsAdminOrReadOnly, AuthorAndStaffOrReadOnly,
                             AdminOnly)
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitlesViewSerializer,
                             ReviewsSerializer, CommentsSerializer,
                             UserSerializer, TokenSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AdminOnly, ]
    http_method_names = ['get', 'list', 'post', 'patch', 'delete', ]
    search_fields = ['username', ]
    lookup_field = 'username'

    @action(detail=False, permission_classes=(IsAuthenticated,),
            methods=['GET', 'PATCH'])
    def me(self, request):
        self.kwargs['username'] = request.user.username
        if request.method == 'PATCH':
            return self.partial_update(request)
        return self.retrieve(request)

    def perform_update(self, serializer):
        if self.action == 'me':
            serializer.save(role=self.request.user.role)
        else:
            serializer.save()


class APITokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = AccessToken.for_user(serializer.validated_data['user'])
        return Response({'token': str(token)})


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = IsAdminOrReadOnly
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitlesViewSerializer
        return TitleSerializer


class ReviewGenreModelMixin(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAdminOrReadOnly
    ]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class CategoryViewSet(ReviewGenreModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ReviewGenreModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = [AuthorAndStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    permission_classes = [AuthorAndStaffOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        review = title.reviews.get(id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
