from rest_framework import serializers
from Users.models import User

# serializer helps django framework to conver complex querry data to native python datatypes

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'