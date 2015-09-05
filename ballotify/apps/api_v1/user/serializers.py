from accounts.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'birthday', 'gender', 'link', 'facebook_id')
        read_only_fields = ('username', 'email',)
