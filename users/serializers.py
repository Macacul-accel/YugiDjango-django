from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=150,
        help_text="Requis. Le mdp doit contenir 1 lettre minuscule + 1 lettre minusclule + 1 chiffre + 1 caractère spécial",
        write_only=True,
    )
    password2 = serializers.CharField(
        max_length=150,
        help_text="Doit être similaire au mot de passe",
        write_only=True,
    )


    class Meta:
        model = User
        fields = (
            'username', 'password', 'password2',
        )
    
    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        try:
            password_validation.validate_password(password, user=self.instance)
        except ValidationError as validation_password_error:
            raise serializers.ValidationError({'password': list(validation_password_error.messages)})
        if password != password2:
            raise serializers.ValidationError({'password': "Les mots de passe ne sont pas similaires"})
        return super(UserSerializer, self).validate(data)
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password2')
        
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user