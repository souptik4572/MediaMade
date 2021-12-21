from rest_framework import serializers

from .models import EndUser


class EndUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EndUser
        fields = ('id', 'name', 'email')
