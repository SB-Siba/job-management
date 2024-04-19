from django import forms
from helpers import utils
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
from django.forms.utils import ValidationError
from django.forms.widgets import MultiWidget

from app_common import models as common_models

class MaxFileSizeValidator:
    def __init__(self, max_size=50*1024):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(f"For performence purpose file-size should not exceed {self.max_size/1024} KB.")


# =================================================== manage coupon  =============================================

# class CouponEntryForm(forms.ModelForm):
#     class Meta:
#         model = common_models.Coupon
#         fields = [
#             'code',
#             'discount_type',
#             'discount_digit',
#             'quantity',
#             'active',

#         ]
    
#     code = forms.CharField(max_length=255)
#     code.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

#     discount_type = forms.ChoiceField(choices= common_models.Coupon.DiscountType, initial="flat")
#     discount_type.widget.attrs.update({'class': 'form-control','type':'text','required':'required'})

#     discount_digit = forms.IntegerField()
#     discount_digit.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Amount or Percentage',"required":"required"})

#     quantity = forms.IntegerField()
#     quantity.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Coupon Quantity',"required":"required"})

#     active = forms.ChoiceField(choices= common_models.Coupon.YESNO, initial="yes")
#     active.widget.attrs.update({'class': 'form-control','type':'text'})

# =================================================== manage catagory  =============================================
class CategoryEntryForm(forms.ModelForm):
    class Meta:
        model = common_models.Category
        fields = [
            'title',
            'description',

        ]
    
    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})


class AudioBookForm(forms.ModelForm):
    class Meta:
        model = common_models.AudioBook
        fields = [
            'title',
            'category',
            'author',
            'narrated_by',
            'description',
            'book_max_price',
            'book_discount_price',
            'release_date',
            'demo_audio_file',
            'language',
            'stock',
            'trending',
            'show_as_new',
            'display_as_bestseller',
            'hide',
            'audiobook_image',

        ]
    
    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    category = forms.ModelChoiceField(queryset = common_models.Category.objects.all())
    category.widget.attrs.update({'class': 'form-control','type':'text'})

    author = forms.CharField(max_length=255)
    author.widget.attrs.update({'class': 'form-control','type':'text'})

    narrated_by = forms.CharField(max_length=255)
    narrated_by.widget.attrs.update({'class': 'form-control','type':'text'})

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})


    book_max_price = forms.IntegerField()
    book_max_price.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Market Price',"required":"required"})

    book_discount_price = forms.IntegerField()
    book_discount_price.widget.attrs.update({'class': 'form-control','type':'text','placeholder':'Enter Your Discounted Price',"required":"required"})

    release_date = forms.DateField()
    release_date.widget.attrs.update({'class': 'form-control','type':'date',"required":"required"})
    
    demo_audio_file = forms.FileField(label='Select an audio file')
    demo_audio_file.widget.attrs.update({'class': 'form-control','type':'file'})

    language = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    language.widget.attrs.update({'class': 'form-control','type':'text'})

    stock = forms.IntegerField(required=True)
    stock.widget.attrs.update({'class': 'form-control','type':'number'})


    trending = forms.ChoiceField(choices=common_models.AudioBook.YESNO, initial= 'no')
    trending.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    show_as_new = forms.ChoiceField(choices=common_models.AudioBook.YESNO, initial= 'no')
    show_as_new.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    display_as_bestseller = forms.ChoiceField(choices=common_models.AudioBook.YESNO, initial= 'no')
    display_as_bestseller.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    hide = forms.ChoiceField(choices=common_models.AudioBook.YESNO, initial= 'no')
    hide.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    audiobook_image = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png']),MaxFileSizeValidator(50*1024)]) # 20 = kb
    audiobook_image.widget.attrs.update({'class': 'form-control','type':'file'})

    
    
class EpisodeForm(forms.ModelForm):

    class Meta:
        model = common_models.Episode
        fields = ['e_id','title','description','audio_file','audiobook']

    e_id = forms.IntegerField(required=True)
    e_id.widget.attrs.update({'class': 'form-control','type':'number'})

    title = forms.CharField(max_length=255)
    title.widget.attrs.update({'class': 'form-control','type':'text',"required":"required"})

    description = forms.CharField(required=False, widget=forms.Textarea(attrs={"class":"form-control","rows":"2"}))
    description.widget.attrs.update({'class': 'form-control','type':'text'})

    audio_file = forms.FileField(label='Select an audio file')
    audio_file.widget.attrs.update({'class': 'form-control','type':'file'})

    audiobook = forms.ModelChoiceField(queryset = common_models.AudioBook.objects.all())
    audiobook.widget.attrs.update({'class': 'form-control','type':'text'})


