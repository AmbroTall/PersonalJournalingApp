from django.db.models import Count
from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Category, JournalEntry
from .serializers import CategorySerializer, JournalEntrySerializer, EntrySummarySerializer, CategorySummarySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalEntryListCreateView(generics.ListCreateAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class JournalEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JournalEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JournalEntry.objects.filter(user=self.request.user)

class EntrySummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Aggregate entries by date for the authenticated user
        entries = (
            JournalEntry.objects
            .filter(user=request.user)
            .values('created_at__date')
            .annotate(count=Count('id'))
            .order_by('created_at__date')
        )
        # Format data for serializer
        summary_data = [{'date': entry['created_at__date'], 'count': entry['count']} for entry in entries]
        serializer = EntrySummarySerializer(summary_data, many=True)
        return Response(serializer.data)

class CategorySummaryView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        entries = (
            JournalEntry.objects
            .filter(user=request.user)
            .values('category__name')
            .annotate(count=Count('id'))
            .order_by('category__name')
        )
        # Handle uncategorized entries
        summary_data = [
            {'category_name': entry['category__name'] or 'Uncategorized', 'count': entry['count']}
            for entry in entries
        ]
        serializer =    CategorySummarySerializer(summary_data, many=True)
        return Response(serializer.data)