from django.db import models
from django.contrib.auth.models import User

# class ToMicroController(models.Model):
#     bldc    = models.CharField(max_length=10, default="BLDC1")
#     speed   = models.IntegerField()
#     date    = models.DateTimeField(auto_now_add=True, blank=True)
#     user    = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)

#     def __str__(self):
#         return self.date


class ProjectModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=750)
    write_api = models.CharField(max_length=10)
    # read_api = models.CharField(max_length=10)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True)
    field = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class FromMicroController(models.Model):
    project = models.ForeignKey(ProjectModel, on_delete=models.CASCADE, blank=True)
    data   = models.IntegerField()
    date    = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.date


# class ApiModule(models.Model):
#     write_Api   = models.CharField(max_length=10)
#     read_Api    = models.CharField(max_length=10)

#     def __str__(self):
#         return self.write_Api

