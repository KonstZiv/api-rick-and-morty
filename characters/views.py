import random

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from characters.models import Character
from characters.serializers import CharacterSerializer


# Create your views here.
@extend_schema(
    responses={status.HTTP_200_OK: CharacterSerializer},
)
@api_view(["GET"])
def get_random_character_view(request: Request) -> Response:
    """Get random character from Rick&Morty world."""
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

    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="inc_in_name",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filtering by character inclusions in the name parameter (insensitive).",
                examples=[
                    OpenApiExample(
                        "Example:",
                        summary="Search with passing parameters",
                        description="Search for all characters whole name includes 'god'",
                        value="god",
                    ),
                ],
            ),
        ]
    )
    def get(self, request, *args, **kwargs):
        """List characters with filter by name."""
        return super().get(request, *args, **kwargs)
