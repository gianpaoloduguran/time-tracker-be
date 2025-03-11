from django.contrib import admin

from time_tracking.models import ProjectsModel


@admin.register(ProjectsModel)
class ProjectsModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
    )
