
from helpers import utils, api_permission

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc

from app_common import models as common_model
from . import serializer as address_serializer
from .serializer import AddressAddSerializer
 
class AddressManage(APIView):

    permission_classes = [api_permission.is_authenticated]
    serializer_class= address_serializer.AddressAddSerializer
    model= common_model.User

    @swagger_auto_schema(
        tags=["address"],
        operation_description="Address Add API..",
        request_body=AddressAddSerializer,
    )

    def post(self, request):
        
        user = request.user
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user.address[request.data['address_title']] = request.data
            user.save()
            return Response({
                "status":200,
                "message": "Address is added..",
                "address_list":[value for key, value in user.address.items()]
                
            })
        else:
            error_list = utils.serilalizer_error_list(serializer.errors)
            return Response({
                "status":400,
                "error":error_list
            })


    @swagger_auto_schema(
        tags=["address"],
        operation_description="Address List..",
    )
    def get(self, request):
        
        user = request.user

        return Response({
            "status":200,
            "address_list":[value for key, value in user.address.items()],
            
        })


    @swagger_auto_schema(
        tags=["address"],
        operation_description="Address List..",
        manual_parameters=swagger_doc.address_delete,
    )
    def delete(self, request):
        address_title = request.GET.get('address_title')
        user = request.user
        user.address.pop(address_title)
        user.save()
        return Response({
            "status":200,
            "message":"Your Address is deleted....",
            "address_list":[value for key, value in user.address.items()],
            
        })


    @swagger_auto_schema(
        tags=["address"],
        operation_description="Address update API..",
        request_body=AddressAddSerializer,
    )

    def put(self, request):
        
        user = request.user
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            user.address[request.data['address_title']] = request.data
            user.save()
            return Response({
                "status":200,
                "message": "Address is added..",
                "address_list":[value for key, value in user.address.items()]
                
            })
        else:
            error_list = utils.serilalizer_error_list(serializer.errors)
            return Response({
                "status":400,
                "error":error_list
            })