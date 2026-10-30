from rest_framework import serializers

class GoogleAuthSerializer(serializers.Serializer):
    code = serializers.CharField(required=True, trim_whitespace=True)
