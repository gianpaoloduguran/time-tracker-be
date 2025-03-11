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
    date_worked = models.TimeField()
    work_description = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    minutes = models.IntegerField()

    @property
    def duration(self):
        return self.end_time - self.start_time
