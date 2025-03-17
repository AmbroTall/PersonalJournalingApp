from django.urls import path
from .views import CategoryListCreateView, JournalEntryListCreateView, JournalEntryDetailView, EntrySummaryView, \
    CategorySummaryView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('entries/', JournalEntryListCreateView.as_view(), name='entry-list-create'),
    path('entries/<int:pk>/', JournalEntryDetailView.as_view(), name='entry-detail'),
    path('entries/summary/', EntrySummaryView.as_view(), name='entry-summary'),
    path('entries/category-summary/', CategorySummaryView.as_view(), name='category-summary'),
]