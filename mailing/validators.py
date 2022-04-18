import re
from rest_framework import serializers


class PhoneNumberValidator:
    def __init__(self, value):
        self.__call__(value)

    def __call__(self, value):
        if not re.match(r'^7([0-9]){9}$', value):
            raise serializers.ValidationError("Incorrect phone number")
