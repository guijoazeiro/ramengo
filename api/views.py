from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import OrderSerializers

BROTHS = ["Shoyu", "Miso", "Tonkotsu"]
PROTEINS = ["Chicken", "Pork", "Tofu"]

class BrothList(APIView):
    def get(self, request):
        return Response(BROTHS)

class ProteinList(APIView):
    def get(self, request):
        return Response(PROTEINS)

class OrderCreate(APIView):
    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            broth = serializer.validated_data['broth']
            protein = serializer.validated_data['protein']
            if broth not in BROTHS or protein not in PROTEINS:
                return Response({"error": "Invalid broth or protein selection."}, status=status.HTTP_400_BAD_REQUEST)
            
            response = requests.post(
                'https://api.tech.redventures.com.br/orders/generate-id',
                headers={'x-api-key': 'ZtVdh8XQ2U8pWI2gmZ7f796Vh8GllXoN7mr0djNf'}
            )
            print(response.json())
            if response.status_code == 200:
                order_id = response.json().get('orderId')
                return Response({"order_id": order_id, "broth": broth, "protein": protein})
            else:
                return Response({"error": "Failed to generate order ID."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
