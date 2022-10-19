from rest_framework import serializers
from genres.models import Genre

from genres.serializers import GenreSerializer
from movies.models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    premiere = serializers.DateField()
    duration = serializers.CharField(max_length=10)
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()
    genres = GenreSerializer(many=True)

    def create(self, validated_data):
        genres_list = validated_data.pop("genres")

        movie = Movie.objects.create(**validated_data)

        for genre_dict in genres_list:
            genre_obj, _ = Genre.objects.get_or_create(**genre_dict)
            movie.genres.add(genre_obj)

        movie.save()

        return movie

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "genres":
                genres = []
                for genre_dict in value:
                    genre_obj, _ = Genre.objects.get_or_create(**genre_dict)
                    genres.append(genre_obj)
                instance.genres.set(genres)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance
