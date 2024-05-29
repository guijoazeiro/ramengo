from rest_framework import serializers

class OrderSerializers(serializers.Serializer):
    broth = serializers.CharField(max_length=100)
    protein = serializers.CharField(max_length=100)