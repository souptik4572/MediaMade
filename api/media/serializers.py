from rest_framework import serializers

from .models import Media


class MediaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'file', 'caption', 'type', 'created_at', 'updated_at')
