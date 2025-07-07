import base64
from rest_framework import serializers

class Base64ImageField(serializers.Field):
    def to_internal_value(self, data):
        # expect data like "data:image/png;base64,..." or plain Base64
        if "," in data:
            header, data = data.split(",", 1)
        try:
            return base64.b64decode(data)
        except Exception:
            raise serializers.ValidationError("Invalid base64 image")
    def to_representation(self, value):
        return base64.b64encode(value).decode()
