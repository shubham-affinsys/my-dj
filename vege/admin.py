from django.contrib import admin
from .models import *

admin.site.register(Recipe)
admin.site.register(Student)
admin.site.register(StudentID)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(SubjectMarks)
admin.site.register(Todo)

class SubjectMarkAdmin(admin.ModelAdmin):
    list_display = ['student', 'subject', 'marks']  # change how values are listed in admin panel #overwritten method
