from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Group
from .serializers import GroupSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_list(request):
    try:
        title = request.query_params.get('title', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        groups = Group.objects.filter(is_deleted=False) 
        if title:
            groups = groups.filter(title__icontains=title)
        if order_by:
            groups = groups.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                groups = groups[:limit]
            except ValueError:
                return Response({"error": "Invalid limit"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def group_detail(request, pk):
    try:
        group = Group.objects.get(pk=pk, is_deleted=False)
        serializer = GroupSerializer(group)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def group_create(request):
    try:
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def group_update(request, pk):
    try:
        group = Group.objects.get(pk=pk, is_deleted=False)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def group_delete(request, pk):
    try:
        group = Group.objects.get(pk=pk, is_deleted=False)
        group.is_deleted = True  
        group.save()
        return Response({"status": "Group deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Group.DoesNotExist:
        return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
