from drf_yasg import openapi

job_filter = [
    openapi.Parameter(
        "filter_by", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
]


signup_post = [

    openapi.Parameter(
        "full_name", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "email", openapi.IN_QUERY, required=True,format=openapi.FORMAT_EMAIL ,type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "contact", openapi.IN_QUERY, required=True, type=openapi.TYPE_NUMBER
    ),
    openapi.Parameter(
        "password", openapi.IN_QUERY,format = openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING
    ),
        openapi.Parameter(
        "confirm_password", openapi.IN_QUERY,format = openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING
    ),
]
