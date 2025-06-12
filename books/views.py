from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .models import Book, ReadingList, ReadingListItem
from .serializers import UserSerializer, BookSerializer, ReadingListSerializer, ReadingListItemSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class ReadingListViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingListSerializer

    def get_queryset(self):
        return ReadingList.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReadingListItemViewSet(viewsets.ModelViewSet):
    serializer_class = ReadingListItemSerializer

    def get_queryset(self):
        return ReadingListItem.objects.filter(reading_list__user=self.request.user)

    @action(detail=True, methods=['post'])
    def reorder(self, request, pk=None):
        try:
            item = self.get_object()
            new_order = request.data.get('order')
            if new_order is not None:
                item.order = new_order
                item.save()
                return Response({'status': 'order updated'})
            return Response({'error': 'order not provided'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)