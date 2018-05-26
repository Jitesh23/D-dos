from rest_framework import serializers
from users.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ('image','users',)
