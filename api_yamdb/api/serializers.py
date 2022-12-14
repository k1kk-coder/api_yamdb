from rest_framework import serializers, exceptions
from django.db.models import Avg
from rest_framework.validators import UniqueValidator
from reviews.models import (Category, Comment, Genre, Review, Title,
                            User)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = GenreSerializer(value)
        return serializer.data


class CategoryField(serializers.SlugRelatedField):
    def to_representation(self, value):
        serializer = CategorySerializer(value)
        return serializer.data


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategoryField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    genre = GenreField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all())

    class Meta:
        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    text = serializers.CharField()

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)

    def validate(self, review):
        if self.context['request'].method != 'POST':
            return review

        title_pk = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user

        if Review.objects.filter(author=author, title=title_pk).exists():
            raise serializers.ValidationError(
                '???? ?????? ?????????????????? ?????????? ?? ?????????????? ????????????????????????.')
        return review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class SignupSerializer(serializers.ModelSerializer):
    forbidden_characters = "!@#$%+=&?"
    username = serializers.CharField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError(
                f"Your username can't be {attrs.get('username')}")

        if User.objects.filter(
            username__iexact=attrs.get('username')
        ).exists():
            raise serializers.ValidationError(
                f'User with nickname {attrs.get("username")} already exists.'
            )

        if User.objects.filter(email__iexact=attrs.get('email')).exists():
            raise serializers.ValidationError(
                f'User with email {attrs.get("email")} already exists.'
            )

        for symbol in attrs.get('username'):
            if symbol in self.forbidden_characters:
                raise serializers.ValidationError(
                    f'This symbol: {symbol} is forbidden'
                )

        return attrs


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=300)

    def validate(self, attrs):
        user = attrs.get('username')
        if not User.objects.filter(username=user).exists():
            raise exceptions.NotFound('There is not such user')
        return attrs
