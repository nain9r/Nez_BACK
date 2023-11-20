from rest_framework import serializers
from .models import AudioFile, Text


class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = ['audio']


class TextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Text
        fields = '__all__'