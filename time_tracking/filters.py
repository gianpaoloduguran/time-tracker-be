import django_filters
from time_tracking.models import TimeTrackingModel


class TimeTrackingModelFilter(django_filters.FilterSet):
    """The filter class for time tracking"""

    start_date = django_filters.DateFilter(
        field_name="date_worked__date", lookup_expr="gte", label="Start Date"
    )
    end_date = django_filters.DateFilter(
        field_name="date_worked__date", lookup_expr="lte", label="End Date"
    )
    project = django_filters.NumberFilter(field_name="project__id", lookup_expr="exact")

    class Meta:
        model = TimeTrackingModel
        fields = ["start_date", "end_date", "project"]
