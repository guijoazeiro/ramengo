from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from .serializers import OrderSerializers
import os
from dotenv import load_dotenv

load_dotenv()

BROTHS = ["Shoyu", "Miso", "Tonkotsu"]
PROTEINS = ["Chicken", "Pork", "Tofu"]

class BrothList(APIView):
    def get(self, request):
        return Response(BROTHS, content_type="application/json")

class ProteinList(APIView):
    def get(self, request):
        return Response(PROTEINS, content_type="application/json")

class OrderCreate(APIView):
    def post(self, request):
        serializer = OrderSerializers(data=request.data)
        if serializer.is_valid():
            broth = serializer.validated_data['broth']
            protein = serializer.validated_data['protein']
            if broth not in BROTHS or protein not in PROTEINS:
                return Response({"error": "Invalid broth or protein selection."}, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")
            
            api_key = os.getenv('API_KEY')
            if not api_key:
                return Response({"error": "API Key not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
            
            try:
                response = requests.post(
                    'https://api.tech.redventures.com.br/orders/generate-id',
                    headers={'x-api-key': api_key}
                )
                response.raise_for_status()
                order_id = response.json().get('order_id')
                return Response({"order_id": order_id, "broth": broth, "protein": protein}, content_type="application/json")
            except requests.exceptions.RequestException as e:
                return Response({"error": "Failed to generate order ID."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, content_type="application/json")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, content_type="application/json")