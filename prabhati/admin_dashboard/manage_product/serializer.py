from rest_framework import serializers

from app_common import models as common_models

class CatagorySerializer(serializers.ModelSerializer):

    class Meta:
        model = common_models.Catagory
        fields = "__all__"

class jobSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = common_models.Job
        fields = "__all__"
   