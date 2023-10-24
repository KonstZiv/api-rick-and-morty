import random

from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


# Create your views here.
@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    rnd_pk = random.choice(Character.objects.values_list("id", flat=True))
    rnd_character = Character.objects.get(pk=rnd_pk)
    serializer = CharacterSerializer(rnd_character)
    return Response(serializer.data, status=status.HTTP_200_OK)


class CharacterListView(generics.ListAPIView):
    serializer_class = CharacterSerializer

    def get_queryset(self):
        queryset = Character.objects.all()
        inc_in_name = self.request.query_params.get("inc_in_name")
        if inc_in_name is not None:
            queryset = queryset.filter(name__icontains=inc_in_name)
        return queryset
