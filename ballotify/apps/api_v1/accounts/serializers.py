from accounts.models import User

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'link', 'facebook_id')
        read_only_fields = ('name', 'link', 'facebook_id')
