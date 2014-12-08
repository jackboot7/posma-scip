#from datetime import datetime

#from django.conf import settings

from apps.api.serializers import UserSerializer


def jwt_payload_handler(user):
    """
    Function that builds a user-info object when encoding the tokens for JWT authentication
    """
    serializer = UserSerializer(user)
    data = serializer.data
    return data
