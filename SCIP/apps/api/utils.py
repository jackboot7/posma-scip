#from datetime import datetime

#from django.conf import settings

from apps.api.serializers import UserSerializer


def jwt_payload_handler(user):
    """
    Function that builds a user-info object when encoding the tokens for JWT authentication
    """
    serializer = UserSerializer(user)
    serializer.fields.pop('last_workday')
    serializer.fields.pop('is_working')
    serializer.fields.pop('average_hours_worked')
    data = serializer.data
    return data
