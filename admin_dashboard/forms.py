# from django import forms
# from helpers import utils
# from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator
# from django.forms.utils import ValidationError

# from app_common import models as common_models

# class MaxFileSizeValidator:
#     def __init__(self, max_size=50*1024):
#         self.max_size = max_size

#     def __call__(self, file):
#         if file.size > self.max_size:
#             raise ValidationError(f"For performence purpose file-size should not exceed {self.max_size/1024} KB.")



# class BannerForm(forms.ModelForm):
#     class Meta:
#         model = common_models.Banner
#         fields = "__all__"

#     image = forms.FileField(
#         required= True,
#         validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg','png']),  MaxFileSizeValidator(50*1024)]
#     ) # 50 = kb

#     image.widget.attrs.update({'class': 'form-control','type':'file'})

#     show = forms.ChoiceField(choices= common_models.Banner.YESNO)
#     show.widget.attrs.update({'class': 'form-control','type':'text'})

#     sl_no = forms.IntegerField()
#     sl_no.widget.attrs.update({'class': 'form-control','type':'number','placeholder':'Banner Display Order',"required":"required"})