import json
from django.http import JsonResponse

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        response_data = {
            'error': 'Internal Server Error',
            'message': str(exception)
        }
        return JsonResponse(response_data, status=500)
