from accounts.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'name', 'birthday', 'gender', 'link', 'facebook_id')
        read_only_fields = ('email',)
