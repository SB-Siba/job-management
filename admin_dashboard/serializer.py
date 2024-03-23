from rest_framework import serializers

from app_common import models as common_models

class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = common_models.Banner
        fields = "__all__"