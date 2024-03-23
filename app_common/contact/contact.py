
from django.utils.decorators import method_decorator

from helpers import utils, api_permission

# for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
# -------------------------------------------- custom import
from .. import swagger_doc
from .serializer import ContactMessageSerializer
from app_common import models as common_model


class AllMessageListApi(APIView):

    permission_classes = [api_permission.is_authenticated]
    pagination_class = utils.CustomPagination(50)
    model = common_model.ContactMessage
    serializer_class = ContactMessageSerializer

    @swagger_auto_schema(
        tags=["contact_message"],
        operation_description="Message Filter and list (by default it will show all message)",
        manual_parameters=swagger_doc.contact_mesage_filter,
    )   
    def get(self,request):
        filter_by = request.GET.get('filter_by', None)
        query_dict = {"user":request.user,}
        if filter_by:
            query_dict['status'] = filter_by
        
        print(query_dict)
        message_list = self.model.objects.filter(**query_dict).order_by('-id')
        
        paginator = self.pagination_class
        page = paginator.paginate_queryset(message_list, request)
        serializer_data = self.serializer_class(page, many=True).data
        return Response({
            "status":200,
            "conversation_list":serializer_data,
            "pagination_meta_data": paginator.pagination_meta_data(),
        })
    


class MessageCreateApi(APIView):

    permission_classes = [api_permission.is_authenticated]
    model = common_model.ContactMessage
    serializer_class = ContactMessageSerializer

    @swagger_auto_schema(
        tags=["contact_message"],
        operation_description="Message Creation api",
        manual_parameters=swagger_doc.contact_message_create,
    )
    
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            obj = serializer.save(
                user = request.user
            )
            return Response({
                "status":200,
                "message":"Hi, we got your message, You will get call ASAP",
                "message_obj": self.serializer_class(obj).data
            })
        else:
            errors = []
            for field, field_errors in serializer.errors.items():
                for field_error in field_errors:
                    errors.append(f"{field}: {field_error}")
            
            return Response({
                "status":400,
                "error":errors,
            })
