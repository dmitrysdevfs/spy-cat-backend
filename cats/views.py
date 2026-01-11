from rest_framework import viewsets, status, response, decorators
from .models import SpyCat, Mission, Target
from .serializers import SpyCatSerializer, MissionSerializer, TargetSerializer

class SpyCatViewSet(viewsets.ModelViewSet):
    queryset = SpyCat.objects.all()
    serializer_class = SpyCatSerializer

class MissionViewSet(viewsets.ModelViewSet):
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.cat is not None:
            return response.Response(
                {"error": "Cannot delete mission that is already assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @decorators.action(detail=True, methods=['patch'], url_path='assign-cat')
    def assign_cat(self, request, pk=None):
        mission = self.get_object()
        cat_id = request.data.get('cat')
        
        if not cat_id:
            return response.Response({"error": "Cat ID is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cat = SpyCat.objects.get(id=cat_id)
        except SpyCat.DoesNotExist:
            return response.Response({"error": "Cat not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if Mission.objects.filter(cat=cat).exclude(status='completed').exists():
            return response.Response({"error": "Cat already has an active mission."}, status=status.HTTP_400_BAD_REQUEST)
        
        mission.cat = cat
        mission.status = 'active'
        mission.save()
        
        return response.Response(MissionSerializer(mission).data)

    @decorators.action(detail=True, methods=['patch'], url_path='targets/(?P<target_id>[^/.]+)')
    def update_target(self, request, pk=None, target_id=None):
        mission = self.get_object()
        try:
            target = mission.targets.get(id=target_id)
        except Target.DoesNotExist:
            return response.Response({"error": "Target not found in this mission."}, status=status.HTTP_404_NOT_FOUND)
        
        notes = request.data.get('notes')
        target_status = request.data.get('status')
        
        if notes:
            if target.status == 'completed' or mission.status == 'completed':
                return response.Response({"error": "Notes cannot be updated because the target or mission is completed."}, status=status.HTTP_400_BAD_REQUEST)
            target.notes = notes
            
        if target_status:
            target.status = target_status
            
        target.save()
        
        if not mission.targets.exclude(status='completed').exists():
            mission.status = 'completed'
            mission.save()
            
        return response.Response(TargetSerializer(target).data)
