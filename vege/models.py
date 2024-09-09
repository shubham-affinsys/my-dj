import uuid

from django.db import models
from django.contrib.auth.models import User
from core import media_cdn
from cloudinary.models import CloudinaryField

# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,blank=True)
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.TextField()
    recipe_view_count = models.IntegerField(default=1)

    # recipe_image = models.ImageField(upload_to="recipes/")  
    recipe_image = CloudinaryField('image',folder="recipes/") # CloudField automatically handles uload and retrival of images through cloudinary
    
    
    class Meta:
        ordering = ['user'] 


class Department(models.Model):
    department = models.CharField(max_length=100)

    def __str__(self):
        return self.department

    class Meta:
        ordering = ['department']  # data will be stored in a specific order department name in this case


class StudentID(models.Model):
    student_id = models.CharField(max_length=100)

    def __str__(self):
        return self.student_id

class Student(models.Model):
    department = models.ForeignKey(Department, related_name='depart', on_delete=models.CASCADE)
    student_id = models.OneToOneField(StudentID, related_name='studentid', on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField(unique=True)
    student_age = models.IntegerField(default=18)
    student_address = models.TextField()

    def __str__(self):
        return self.student_name

    class Meta:
        ordering = ['student_name']
        verbose_name = "student"


class Subject(models.Model):
    subject_name = models.CharField(max_length=30)

    def __str__(self):
        return self.subject_name

class SubjectMarks(models.Model):
    student = models.ForeignKey(Student, related_name='studentmarks', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f'{self.student.student_name} {self.subject.subject_name}'

    class Meta:
        unique_together = ['student', #
                           'subject']  # every marks for subject will be unique and new subject of same name will not be created


# default django models does not have uuid
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True  # so that we can use it as a class

class Todo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    todo_title = models.CharField(max_length=100)
    todo_description = models.TextField()
    is_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['user'] 

class TimingTodo(BaseModel):
    todo = models.ForeignKey(Todo,on_delete=models.CASCADE)
    timming = models.DateField()