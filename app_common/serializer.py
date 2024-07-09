from rest_framework import serializers


from . import models as common_models

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.User
        fields = [
            'full_name',
            'email',
            'contact',
            'password',

        ]

        extra_kwargs = {
            'full_name': {'required': True},
            'email': {'required': True},
            'contact': {'required': True},
            'password': {'required': True},
            }

    def validate(self, data):
        
        if len(data['password']) < 8:
            raise serializers.ValidationError('Password Length is less than 8..')


        return data
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.User
        fields = [
            'contact',
            'password',
        ]
        extra_kwargs = {
            'contact': {'required': True},
            'password': {'required': True},
            }
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = common_models.User
        exclude = ["password"]



class ForgotPasswordSerializer(serializers.Serializer):

    contact = serializers.CharField(max_length = 10, required =True)
    
class NewPasswordSerializer(serializers.Serializer):

    password1 = serializers.CharField(max_length = 255, required =True)
    password2 = serializers.CharField(max_length = 255, required =True)

    def validate(self, data):
        # Check if the passwords match
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The passwords do not match.")
        
        if len(data['password1']) < 6:
            raise serializers.ValidationError("Your Password is very weak")
        
        return data