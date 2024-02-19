from rest_framework import serializers
from .models import Note, NoteChange

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('_all_')

class NoteChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteChange
        fields = ('_all_')