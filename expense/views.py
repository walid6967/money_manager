from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Expense
from .serializers import ExpenseSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_list(request):
    try:
        text = request.query_params.get('text', None)
        amount = request.query_params.get('amount', None)
        date = request.query_params.get('date', None)
        category = request.query_params.get('category', None)
        limit = request.query_params.get('limit', None)
        order_by = request.query_params.get('order_by', None)
        expenses = Expense.objects.filter(is_deleted=False)
        if text:
            expenses = expenses.filter(text__icontains=text)
        if amount:
            try:
                amount = int(amount)
                expenses = expenses.filter(amount=amount)
            except ValueError:
                return Response({"error": "Invalid amount value"}, status=status.HTTP_400_BAD_REQUEST)
        if date:
            expenses = expenses.filter(date=date)
        if category:
            expenses = expenses.filter(category__icontains=category)
        if order_by:
            expenses = expenses.order_by(order_by)
        if limit:
            try:
                limit = int(limit)
                expenses = expenses[:limit]
            except ValueError:
                return Response({"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def expense_detail(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, is_deleted=False)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def expense_create(request):
    try:
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def expense_update(request, pk):
    try:
        expense = Expense.objects.get(pk=pk, is_deleted=False)
        serializer = ExpenseSerializer(expense, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def expense_delete(request, pk):
    try:
        expense = Expense.objects.get(pk=pk)
        expense.is_deleted = True  # Soft delete
        expense.save()
        return Response({"status": "Expense deleted successfully"},status=status.HTTP_204_NO_CONTENT)
    except Expense.DoesNotExist:
        return Response({"error": "Expense not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
