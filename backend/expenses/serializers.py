from rest_framework import serializers
from .models import Expense

class ExpenseSerializer(serializers.ModelSerializer):
    ai_predicted = serializers.SerializerMethodField()
    ai_confidence = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'ai_predicted_category', 'date', 'created_at', 'updated_at', 'ai_predicted', 'ai_confidence']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_ai_predicted(self, obj):
        return obj.ai_predicted_category is not None

    def create(self, validated_data):
        # Handle frontend fields
        ai_predicted_input = validated_data.pop('ai_predicted', False) if 'ai_predicted' in validated_data else False
        ai_confidence = validated_data.pop('ai_confidence', None)
        
        if ai_predicted_input:
            validated_data['ai_predicted_category'] = validated_data['category']
        
        return super().create(validated_data)