from django.http import JsonResponse

from designs.models import Propulsion


def site_info(request):
    site_name = 'Boatplans.cc'
    # slug label
    propulsions = [
        {'slug': propulsion.slug, 'longName': propulsion.long_name, 'lengths': []}
        for propulsion in Propulsion.objects.all()
    ]
    return JsonResponse(
        {
            'siteName': site_name,
            'propulsions': propulsions,
        }
    )
