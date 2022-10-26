from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title, User

from api.filters import TitlesFilter
from api.permissions import (AdminOrGetRequestPermission, AdminPermission,
                             AuthorOrStaffPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ObtainTokenSerializer,
                             ReviewSerializer, SignupSerializer,
                             TitleSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (AdminOrGetRequestPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitlesFilter


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrGetRequestPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrStaffPermission,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (permissions.IsAuthenticated,)
        return super(ReviewViewSet, self).get_permissions()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CategoryViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrGetRequestPermission,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrStaffPermission,)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        return review.comments.all()

    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = (permissions.IsAuthenticated,)
        return super(CommentViewSet, self).get_permissions()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id)
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminPermission, )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.user.role == "admin":
            serializer_class = UserSerializer
        return serializer_class

    @action(
        methods=["get", "patch"], detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role, partial=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", ])
@permission_classes([AllowAny])
def registration(request):
    serializer = SignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    conf_code = default_token_generator.make_token(user)
    send_mail(
        subject='Registration',
        message=f'Your code for obtain API token: {conf_code}',
        from_email=None,
        recipient_list=[user.email],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", ])
@permission_classes([AllowAny])
def obtain_token(request):
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    conf_code = serializer.validated_data["confirmation_code"]
    if default_token_generator.check_token(user, conf_code):
        inside_token = RefreshToken.for_user(user)
        access_token = {'token': str(inside_token.access_token)}
        return Response(access_token, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
