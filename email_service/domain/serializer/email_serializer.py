from rest_framework import serializers

from email_service.domain.model.email import Email


class EmailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    to = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    body = serializers.CharField()

    def create(self, validated_data) -> Email:
        return Email(**validated_data)
