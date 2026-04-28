from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Link
from .serializers import LinkSerializer
from django.contrib.auth.models import AnonymousUser
import string
import random

def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@api_view(['POST'])
def create_short_link(request):
    if isinstance(request.user, AnonymousUser):
        return Response({"error": "Authentication required"}, status=401)

    serializer = LinkSerializer(data=request.data)

    if serializer.is_valid():
        short_code = generate_code()

        link = serializer.save(
            user=request.user,
            short_code=short_code
        )

        return Response(LinkSerializer(link).data, status=201)

    return Response(serializer.errors, status=400)
