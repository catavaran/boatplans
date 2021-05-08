from django_filters import rest_framework as filters

from designs.form_fields import clean_imperial_size_value
from designs.models import Design, Propulsion

class SizeFilter(filters.CharFilter):
    def filter(self, qs, value):
        if not value:
            return qs
        if 'ft' in value:
            value = clean_imperial_size_value(value)
        else:
            value = int(value) * 1000
        lookup = '{field}__{expr}'.format(field=self.field_name, expr=self.lookup_expr)
        return self.get_method(qs)(**{lookup: value})


class DesignFilterSet(filters.FilterSet):
    loa_min = SizeFilter(field_name='loa', lookup_expr='gte')
    loa_max = SizeFilter(field_name='loa', lookup_expr='lte')
    propulsion = filters.ModelChoiceFilter(
        queryset=Propulsion.objects.all(), to_field_name='slug', required=True
    )

    class Meta:
        model = Design
        fields = ['propulsion']