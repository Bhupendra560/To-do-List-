from rest_framework import serializers
from todolist.settings import STATUS_CHOICES
from .models import Task, Tag

class InputSerializer(serializers.ModelSerializer):
        title = serializers.CharField(required=True)
        status = serializers.ChoiceField(required=True, choices=STATUS_CHOICES)
        description = serializers.CharField(required=True)
        # optional fields
        tags = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
        due_date = serializers.DateField(required=False)
        class Meta:
            model = Task
            exclude = ["timestamp"]

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["value"]
        
class OutputSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = "__all__"
        



            