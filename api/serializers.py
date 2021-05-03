from rest_framework import serializers
from .models import Collections
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = "__all__"
        
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username',  'password')
        