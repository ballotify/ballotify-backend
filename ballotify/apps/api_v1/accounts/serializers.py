from accounts.models import User

from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'name', 'link', 'facebook_id')
        read_only_fields = ('name', 'link', 'facebook_id')

    def validate_username(self, username):
        if not User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User does not exist.")

        return username
