from django.contrib import admin

from time_tracking.models import ProjectsModel, TimeTrackingModel

# Display the models/tables in django admin.


@admin.register(ProjectsModel)
class ProjectsModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )


@admin.register(TimeTrackingModel)
class TimeTrackingModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "user",
    )
