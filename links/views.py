from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Link
from .serializers import LinkSerializer
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect, get_object_or_404
from .models import Link
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

def redirect_link(request, short_code):
    link = get_object_or_404(Link, short_code=short_code)

    # increment click count
    link.click_count += 1
    link.save(update_fields=['click_count'])

    return redirect(link.original_url)
