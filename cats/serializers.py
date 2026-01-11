from rest_framework import serializers
from .models import SpyCat, Mission, Target
from .utils import validate_breed

class SpyCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpyCat
        fields = '__all__'

    def validate_breed(self, value):
        if not validate_breed(value):
            raise serializers.ValidationError(f"'{value}' is not a valid cat breed according to TheCatAPI.")
        return value

    def update(self, instance, validated_data):
        # Restriction: Only allow updating salary
        salary = validated_data.get('salary')
        if len(validated_data) > 1 or (len(validated_data) == 1 and 'salary' not in validated_data):
            raise serializers.ValidationError("Only 'salary' can be updated for a spy cat.")
        
        instance.salary = salary or instance.salary
        instance.save()
        return instance

class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ['id', 'name', 'country', 'notes', 'status']

class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ['id', 'cat', 'status', 'targets']

    def create(self, validated_data):
        targets_data = validated_data.pop('targets')
        if not (1 <= len(targets_data) <= 3):
            raise serializers.ValidationError("A mission must have between 1 and 3 targets.")
        
        mission = Mission.objects.create(**validated_data)
        for target_data in targets_data:
            Target.objects.create(mission=mission, **target_data)
        return mission

    def update(self, instance, validated_data):
        # Handle mission update logic if needed, but primary focus is targets and assignment
        # Specific target updates are handled by a separate view/serializer or action
        return super().update(instance, validated_data)
