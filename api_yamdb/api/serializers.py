import datetime as dt
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from reviews.models import Category, Genre, Title, User, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name',
            'bio', 'role'
        )
        model = User


class UserReadOnlySerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        if User.objects.filter(
            username__iexact=username, email__iexact=email
        ).exists():
            return data
        return data


class SignUpValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email',)
        validators = [UniqueTogetherValidator(queryset=User.objects.all(),
                                              fields=['username', 'email']), ]

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Имя не может быть me')
        if User.objects.filter(username__iexact=username).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже зарегистрирован'
            )
        return username

    def validate_email(self, email):
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                'Пользователь с таким адресом уже зарегистрирован'
            )
        return email


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError('Проверьте вводимый год!')
        return value


class TitlesViewSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=False)
    rating = serializers.IntegerField()

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )
        model = Title
        read_only_fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category'
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ['title']

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if user.reviews.filter(title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя дважды писать отзыв к одному произведению!'
                )
        return data

    def validate_score(self, value):
        if 0 >= value >= 10:
            raise serializers.ValidationError('Проверьте поставленную оценку!')
        return value


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
