from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """Base model class"""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ProjectsModel(BaseModel):
    title = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)


class TimeTrackingModel(BaseModel):

    project = models.ForeignKey(
        ProjectsModel,
        related_name="records",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(User, related_name="records", on_delete=models.CASCADE)
    date_worked = models.DateTimeField()
    work_description = models.CharField(max_length=200)
    hours = models.IntegerField()

    @property
    def project_title(self):
        """Returns the title of the project"""
        return self.project.title
