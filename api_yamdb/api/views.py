from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)

from reviews.models import Category, Genre, Title
from api.filters import TitleFilter
from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleSerializer, TitlesViewSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate()
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