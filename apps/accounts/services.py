from django.core.exceptions import ValidationError

from apps.accounts.models import CustomUser, UserRating


def rate_user(*, from_user: CustomUser, to_user: CustomUser, score: int, comment: str = None) -> UserRating:
    
    if from_user == to_user:
        raise ValidationError("The user cannot rate themselves!")

    if not (1 <= score <= 5):
        raise ValidationError("The score should be between 1 and 5.")

    rating, created = UserRating.objects.update_or_create(
        from_user=from_user,
        to_user=to_user,
        defaults={
            'score': score,
            'comment': comment
        }
    )
    return rating