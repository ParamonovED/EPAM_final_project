from rest_framework import serializers

from .models import Target


class TargetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Target
        fields = ('title', 'wanted_price')
