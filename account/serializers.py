from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions, validators
from rest_framework.serializers import ModelSerializer, Serializer

from core.serializers import BaseModelSerializer

User = get_user_model()


class UserSerializer(BaseModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')


# class UserBaseSerializer(Serializer):
#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField(max_length=30, allow_blank=False, allow_null=True, )
#     last_name = serializers.CharField(max_length=30, allow_blank=False)
#     email = serializers.EmailField(
#         required=True,
#         validators=[
#             validators.UniqueValidator(
#                 queryset=User.objects.all(),
#                 # lookup="icontains"
#             )
#         ]
#     )
#     password = serializers.CharField(write_only=True)
#
#     def validate_password(self, password):
#         if not validate_password(password):
#             raise exceptions.ValidationError("password invalid")
#         return password
#
#
#     def validate_email(self, email):
#         if email.endswith(('@datawiz.io', '@nielsen.com')):
#             raise exceptions.ValidationError(detail='Такі емейли не є доступні')
#         return email
#
#     def validate(self, attrs):
#         attrs = super().validate(attrs)
#         return attrs
#
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.__dict__.update(**validated_data)
#         instance.save()

# user_data = {
#     'first_name': 'Name',
#     'last_name': 'Name'
# }
# user = User.objects.get(id=1)
# serializer = UserSerializer(instance=user, data=user_data, partial=True)
# serializer.is_valid(raise_exception=True)
# serializer.save()