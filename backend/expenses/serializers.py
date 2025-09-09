from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    ai_predicted = serializers.BooleanField(write_only=True, required=False)
    ai_confidence = serializers.FloatField(write_only=True, required=False)
    ai_predicted_read = serializers.SerializerMethodField()
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'ai_predicted_category', 'date', 'created_at', 'updated_at', 'ai_predicted', 'ai_predicted_read', 'ai_confidence']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_ai_predicted_read(self, obj):
        return obj.ai_predicted_category is not None

    def create(self, validated_data):
        # Handle frontend fields
        ai_predicted_input = validated_data.pop('ai_predicted', False)
        ai_confidence = validated_data.pop('ai_confidence', None)
        
        # Set ai_predicted_category if this was AI categorized
        if ai_predicted_input:
            validated_data['ai_predicted_category'] = validated_data['category']
        
        expense = super().create(validated_data)
        print(f"Created expense: {expense.id}, ai_predicted_category: {expense.ai_predicted_category}")  # Debug
        return expense