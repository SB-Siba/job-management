from drf_yasg import openapi
from .models import Order, ContactMessage
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

login_post = [

    openapi.Parameter(
        "contact", openapi.IN_QUERY, required=True, type=openapi.TYPE_NUMBER
    ),
    openapi.Parameter(
        "password", openapi.IN_QUERY,format = openapi.FORMAT_PASSWORD, required=True, type=openapi.TYPE_STRING
    ),

]


# ======================================= checkout ===============================
update_cart = [

    openapi.Parameter(
        "quantity", openapi.IN_QUERY, required=True, type=openapi.TYPE_NUMBER
    ),

]

update_cart = [

    openapi.Parameter(
        "quantity", openapi.IN_QUERY, required=True, type=openapi.TYPE_NUMBER
    ),

]

order_placed = [

    openapi.Parameter(
        "coupon", openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING
    ),

    openapi.Parameter(
        "address_title", openapi.IN_QUERY, required=False, type=openapi.TYPE_NUMBER, description="Title of the selected address"
    ),

    openapi.Parameter(name="payment_status",in_=openapi.IN_QUERY,required=True, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING,enum=[i[0] for i in Order.PaymentStatus], )
    ),
    
    openapi.Parameter(
        "transaction_id", openapi.IN_QUERY, required=False, type=openapi.TYPE_NUMBER, description="Transaction id if online payment"
    ),

]

order_cancel_return_refund = [

    openapi.Parameter(name="order_status",in_=openapi.IN_QUERY,required=True, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING,enum=['Cancel','Refund','Return',], )
    ),

    openapi.Parameter(
        "more_info", openapi.IN_QUERY, required=False, type=openapi.TYPE_NUMBER, description="Why a user want to  cancel the order ?? "
    ),
    

]
# ======================================= address =========================
address_add = [

    openapi.Parameter(
        "address_title", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "contact1", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "contact2", openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "address", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "landmark", openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "district", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
    openapi.Parameter(
        "zip", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING
    ),
]

address_delete = [

    openapi.Parameter(
        "address_title", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING, description = "pass it in query"
    ),
]

# contact_message
contact_mesage_filter = [

    openapi.Parameter(name="filter_by",in_=openapi.IN_QUERY,required=False, type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING,enum=[i[0] for i in ContactMessage.STATUS], )
    ),
]


contact_message_create = [

    openapi.Parameter(
        "order_number", openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING, description = "Order number is not Mandatory "
    ),
    openapi.Parameter(
        "message", openapi.IN_QUERY, required=True, type=openapi.TYPE_STRING, description = "User's message "
    ),
]
