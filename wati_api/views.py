from django.shortcuts import render
from django.views import View
from django.conf import settings
from .whatsapp_api import WatiAPIClient  # Adjust the import if needed

class SendMessageView(View):
    def get(self, request):
        # Get the contact number from query parameters
        contact = request.GET.get('contact')

        # Initialize the WatiAPIClient with base URL and API key
        client = WatiAPIClient(
            base_url=settings.WATI_BASE_URL,
            api_key=settings.WATI_API_KEY
        )
        
        # Example data
        template_name = "new_chat_v1"
        parameters = [
            {"name": "name", "value": "Matthew"}
        ]
        
        # Send the message
        response = client.send_message(contact, template_name, parameters)
        
        # Render the template with the response data
        context = {
            'response': response,
            'phone_number': contact,
            'template_name': template_name,
            'name': 'Matthew'
        }
        return render(request, 'wati_api/send_message.html', context)
