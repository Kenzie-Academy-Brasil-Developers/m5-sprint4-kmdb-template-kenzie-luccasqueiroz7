from rest_framework import serializers
from accounts.models import User
from reviews.models import Review


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=10)
    user = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "movie",
            "user",
            "recomendation",
        ]
        read_only_fields = [
            "id",
            "movie",
        ]
        depth = 0
