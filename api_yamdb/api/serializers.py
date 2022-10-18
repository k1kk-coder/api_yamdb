from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        return round(obj.reviews.aggregate(Avg('score'))['score__avg'])


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        source='author')
    text = serializers.CharField(source='text')

    class Meta:
        model = Review
        fields = '__all__'

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
