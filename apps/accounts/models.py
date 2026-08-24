from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Q

from core.models import BaseModel


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def average_rating(self):
        """Calculates the average user rating"""
        result = self.received_ratings.aggregate(Avg('score'))['score__avg']
        return round(result, 1) if result else 0.0

    @property
    def total_ratings_count(self):
        """Total number of ratings given to the user"""
        return self.received_ratings.count()


class UserRating(BaseModel):
    """User ratings and comments from each other"""
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='given_ratings')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_ratings')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=500, blank=True, null=True)

    class Meta(BaseModel.Meta):
        verbose_name = "User's rating"
        verbose_name_plural = "User's ratings"
        constraints = [
            models.UniqueConstraint(
                fields=['from_user', 'to_user'],
                condition=Q(is_deleted=False),
                name='unique_active_user_rating'
            )
        ]


    def clean(self):
        from django.core.exceptions import ValidationError
        if self.from_user == self.to_user:
            raise ValidationError("The user cannot rate themselves!")

    def __str__(self):
        return f"{self.from_user} -> {self.to_user}: {self.score}★"