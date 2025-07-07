from rest_framework import serializers
from .models import Task, Milestone, ContextEntry

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ["id","title","completed","completedAt"]

class ContextEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContextEntry
        fields = ["id","content","source","timestamp"]


class TaskSerializer(serializers.ModelSerializer):
    milestones     = MilestoneSerializer(many=True, required=False)
    context        = ContextEntrySerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ["id","title","description","status","priority","category","deadline","createdAt","milestones","context"]

    def create(self, validated):
        user = self.context["request"].user
        m_data = validated.pop("milestones", [])
        c_data = validated.pop("context", [])
        task = Task.objects.create(user=user, **validated)

        for m in m_data:
            Milestone.objects.create(task=task, **m)

        for c in c_data:
            ContextEntry.objects.create(task=task, **c)

        return task

    def update(self, instance, validated_data):
        # 1. update scalar fields
        for attr in ("title","description","status","priority","deadline","category"):
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.save()
        
         # 2. update milestones
        if "milestones" in validated_data:
            new_ms = validated_data.pop("milestones")
            # simple strategy: delete all old & re-create
            instance.milestones.all().delete()
            for m in new_ms:
                Milestone.objects.create(task=instance, **m)

        if "context" in validated_data:
            new_ct = validated_data.pop("context")
            instance.context.all().delete()
            for c in new_ct:
                ContextEntry.objects.create(task=instance, **c)
        
        return instance
        # return super().update(instance, validated_data)