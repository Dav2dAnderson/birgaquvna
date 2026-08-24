from django.db import models
from django.contrib.auth import get_user_model

from core.models import BaseModel

User = get_user_model()


class EventType(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta(BaseModel.Meta):
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'


class Event(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    orgonizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    event_type = models.ForeignKey(EventType, on_delete=models.SET_NULL, null=True, related_name='events')
    location = models.CharField(max_length=255)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} by {self.orgonizer.get_full_name}"

    class Meta(BaseModel.Meta):
        verbose_name = 'Event'
        verbose_name_plural = 'Events'