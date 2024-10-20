from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_list(request):
    try:
        title = request.query_params.get('title', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        categories = Category.objects.filter(is_deleted=True)
        if title:
            categories = categories.filter(title__icontains=title)
        if order_by:
            categories = categories.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                categories = categories[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create(request):
    try:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk, is_deleted=False)
        category.is_deleted = True
        category.save()
        return Response({"message": "Category delete succesfully"} ,status=status.HTTP_204_NO_CONTENT)
    except Category.DoesNotExist:
        return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
