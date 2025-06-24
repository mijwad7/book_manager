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
        if self.action in ['create', 'list']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # Restrict users to only their own profile for relevant actions
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return User.objects.filter(id=self.request.user.id)
        return User.objects.none()  # Return empty queryset for list/create to avoid unnecessary data exposure

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({'error': 'You can only view your own profile'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({'error': 'You can only update your own profile'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            return Response({'error': 'You can only delete your own profile'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.created_by != request.user:
            return Response({'error': 'You can only delete your own books'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

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