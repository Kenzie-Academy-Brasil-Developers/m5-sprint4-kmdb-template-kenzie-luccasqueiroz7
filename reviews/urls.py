from django.urls import path

from reviews.views import ReviewMovieIdView, ReviewReviewIdView

urlpatterns = [
    path(
        "movies/<int:movie_id>/reviews/",
        ReviewMovieIdView.as_view(),
    ),
    path(
        "movies/<int:movie_id>/reviews/<int:review_id>/",
        ReviewReviewIdView.as_view(),
    ),
]
