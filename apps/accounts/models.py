from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Q

from core.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError("Phone number is required.")

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        
        return self.create_user(phone_number, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    bio = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

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