from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=127)
    duration = models.CharField(max_length=10)
    premiere = models.DateField(auto_now=False, auto_now_add=False)
    classification = models.IntegerField()
    synopsis = models.TextField()

    genres = models.ManyToManyField(
        "genres.Genre",
        related_name="movies",
    )
