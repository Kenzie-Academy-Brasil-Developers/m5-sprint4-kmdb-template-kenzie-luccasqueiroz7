from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, Request, Response, status
from kmdb.pagination import CustomPageNumberPagination

from movies.models import Movie
from reviews.models import Review
from reviews.serializers import ReviewSerializer

from rest_framework.authentication import TokenAuthentication

from .permissions import IsCriticOwner, MyCustomPermission


class ReviewMovieIdView(APIView, CustomPageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [MyCustomPermission]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = Review.objects.filter(movie=movie.id, user=request.user.id).exists()

        if reviews:
            return Response(
                {"detail": "Review already exists."}, status.HTTP_403_FORBIDDEN
            )

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, movie=movie)

        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)
        reviews = Review.objects.filter(movie=movie.id)

        result_page = self.paginate_queryset(reviews, request, view=self)

        serializer = ReviewSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)


class ReviewReviewIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCriticOwner]

    def get(self, request: Request, movie_id: int, review_id: int):
        review = get_object_or_404(Review, id=review_id)

        serializer = ReviewSerializer(review)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int, review_id: int):
        review = get_object_or_404(Review, id=review_id)

        self.check_object_permissions(request, review.user)

        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
