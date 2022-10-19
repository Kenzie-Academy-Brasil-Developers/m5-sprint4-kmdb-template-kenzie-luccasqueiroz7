from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from accounts.models import User
from accounts.permissions import IsAccountOwner, MyCustomPermission

from accounts.serializers import LoginSerializer, UserSerializer

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from kmdb.pagination import CustomPageNumberPagination


class UserView(APIView):
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserGetView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MyCustomPermission]

    def get(self, request: Request) -> Response:
        users = User.objects.all()

        result_page = self.paginate_queryset(users, request, view=self)

        serializer = UserSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class UserDetailView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        IsAccountOwner,
    ]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:

            token, _ = Token.objects.get_or_create(user=user)

            return Response(
                {"token": token.key},
                status.HTTP_200_OK,
            )

        return Response(
            {
                "detail": "invalid username or password",
            },
            status.HTTP_400_BAD_REQUEST,
        )
