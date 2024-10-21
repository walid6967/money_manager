from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Income
from .serializers import IncomeSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def income_list(request):
    try:
        text = request.query_params.get('text', None)
        amount = request.query_params.get('amount', None)
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        incomes = Income.objects.filter(is_deleted=False)
        if text:
            incomes = incomes.filter(text__icontains=text)
        if amount:
            try:
                amount = int(amount)
                incomes = incomes.filter(amount=amount)
            except ValueError:
                return Response({"error": "Invalid amount value"}, status=status.HTTP_400_BAD_REQUEST)
        if date:
            incomes = incomes.filter(date=date)
        if category:
            incomes = incomes.filter(category__icontains=category)
        if order_by:
            incomes = incomes.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                incomes = incomes[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = IncomeSerializer(incomes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def income_detail(request, pk):
    try:
        income = Income.objects.get(pk=pk, is_deleted=False)
        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Income.DoesNotExist:
        return Response({"error": "Income not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def income_create(request):
    try:
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def income_update(request, pk):
    try:
        income = Income.objects.get(pk=pk, is_deleted=False)
        serializer = IncomeSerializer(income, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Income.DoesNotExist:
        return Response({"error": "Income not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def income_delete(request, pk):
    try:
        income = Income.objects.get(pk=pk, is_deleted=False)
        income.is_deleted = True
        income.delete()
        return Response({"status": "Income deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Income.DoesNotExist:
        return Response({"error": "Income not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
