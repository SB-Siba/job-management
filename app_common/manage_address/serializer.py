
from rest_framework import serializers

class AddressAddSerializer(serializers.Serializer):

    address_title = serializers.CharField(max_length=255, label='')

    contact1 = serializers.IntegerField( label="Contact" )

    contact2 = serializers.IntegerField( label="Optional Country", required= False )

    address = serializers.CharField(max_length=255, label='Full Address')

    landmark = serializers.CharField(max_length=255, required=False)

    district = serializers.CharField(max_length=255,)

    zip = serializers.IntegerField( label="Zip" )

