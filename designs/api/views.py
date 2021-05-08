"""API views for designs app."""

from django.conf import settings
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from designs.api.filters import DesignFilterSet
from designs.api.serializers import (
    DesignCardSerializer,
    DesignListSerializer,
    PropulsionSerializer,
    PropulsionWithLengthsSerializer,
)
from designs.models import Design, Propulsion
from designs.selectors import get_enabled_designs, get_recent_designs


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


class RecentDesignsView(APIView):
    def get(self, *args, **kwargs):
        recent_designs = [
            {
                'propulsion': PropulsionSerializer(propulsion).data,
                'recent': DesignCardSerializer(
                    get_recent_designs(propulsion),
                    many=True,
                ).data,
            }
            for propulsion in Propulsion.objects.all()
        ]
        return Response(recent_designs)


class DesignListView(ListAPIView):
    queryset = get_enabled_designs()
    serializer_class = DesignListSerializer
    filterset_class = DesignFilterSet