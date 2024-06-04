from rest_framework import serializers

from app_common import models as common_models

class CatagorySerializer(serializers.ModelSerializer):

    class Meta:
        model = common_models.Category
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    discount_percentage = serializers.SerializerMethodField()
    def get_discount_percentage(self, obj):
        return f"{obj.discount_percentage} %"
    
    # class Meta:
    #     model = common_models.AudioBook
    #     fields = [
    #         'title',
    #         'category',
    #         'author',
    #         'generation',
    #         'description',
    #         'book_max_price',
    #         'book_discount_price',
    #         'release_date',
    #         'demo_audio_file',
    #         'language',
    #         'stock',
    #         'trending',
    #         'show_as_new',
    #         'display_as_bestseller',
    #         'hide',
    #         'audiobook_image',
    #     ]