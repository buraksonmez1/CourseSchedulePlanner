from django.db import models
from students.models import OpenCoursesForYou, User, AllOpenCourses, OpenCourses


class  Schedule (models.Model):
    opencourse=models.ForeignKey(OpenCoursesForYou,related_name='+', on_delete=models.CASCADE, null=True)
    place_in_schedule=models.CharField(max_length=200)



