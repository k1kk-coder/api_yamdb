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

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Поставьте оценку от 1 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('title',)


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
        read_only_fields = ('role',)


class UserSerializerForAdmin(serializers.ModelSerializer):
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
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate(self, attrs):
        if attrs.get('username') == 'me':
            raise serializers.ValidationError("Your username can't be 'me'")
        return attrs


class ObtainTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    confirmation_code = serializers.CharField(max_length=300)

    def validate(self, attrs):
        user = attrs.get('username')
        # conf_code = attrs.get('confirmation_code')
        if not User.objects.filter(username=user).exists():
            raise exceptions.NotFound('There is not such user')
        # elif conf_code is :
        #     raise serializers.ValidationError('this conf_code not exists')
        return attrs
