from django.contrib import admin

from .models import *

#admin.site.unregister(User)
admin.site.register(User)
admin.site.register(University)
admin.site.register(Student)
admin.site.register(SubjectArea)
admin.site.register(Competency)
admin.site.register(UniversityProgram)
admin.site.register(Company)
admin.site.register(StudentEducation)
admin.site.register(StudentJob)
admin.site.register(StudentCompetency)
admin.site.register(Vacancy)
admin.site.register(SubjectAreaVacancies)
