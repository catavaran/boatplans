"""API views for designs app."""

from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView

from designs.api.serializers import PropulsionWithLengthsSerializer
from designs.models import Propulsion


class SiteInfoView(APIView):

    def get(self, *args, **kwargs):
        propulsions = PropulsionWithLengthsSerializer(
            Propulsion.objects.all(),
            many=True,
        ).data
        return Response(
            {
                'site_name': settings.SITE_NAME,
                'propulsions': propulsions,
            }
        )
