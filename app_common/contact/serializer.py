from rest_framework import serializers
from app_common import models as common_models

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.ContactMessage
        fields = "__all__"
        
        extra_kwargs = {
            'order_number': {'required': False},
            'message': {'required': True},
            }

class ContactMessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.ContactMessage
        fields = [
            "order_number",
            "message",
        ]
        extra_kwargs = {
            'order_number': {'required': False},
            'message': {'required': True},
            }