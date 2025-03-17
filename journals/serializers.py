from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, JournalEntry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class JournalEntrySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = JournalEntry
        fields = ['id', 'title', 'content', 'category', 'category_id', 'created_at', 'updated_at']

class EntrySummarySerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

class CategorySummarySerializer(serializers.Serializer):
    category_name = serializers.CharField()
    count = serializers.IntegerField()