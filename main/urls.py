from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/university/', views.register_university, name='register_university'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/student/', views.register_student, name='register_student'),
    path('profile/', views.profile, name='profile'),
    path('profile/add-program/', views.add_program, name='add_program'),
    path('profile/add-vacancy/', views.add_vacancy, name='add_vacancy'),
    path('get-subjectarea/', views.get_subjectarea, name='get_subjectarea'),
    path('get-universities/', views.get_universities, name='get_universities'),
    path('get-programs/', views.get_programs, name='get_programs'),
    path('get-companies/', views.get_companies, name='get_companies'),
    path('logout/', views.logout, name='logout'),
    path('program/<int:pk>/', views.display_program, name='display_program'),
    path('university/<int:pk>/programs/', views.display_programs, name='display_programs'),
    path('vacancy/<int:pk>/', views.display_vacancy, name='display_vacancy'),
    path('company/<int:pk>/vacancies/', views.display_vacancies, name='display_vacancies'),
    path('profile/verify-students/', views.verify_students, name='verify_students'),
    path('profile/verify-students-jobs/', views.verify_students_jobs, name='verify_students_jobs'),
    path('profile/verify-student-competencies/<int:pk>/', views.verify_student_competencies, name='verify_student_competencies'),
    path('company/<int:pk>/', views.display_company, name='display_company'),
    path('university/<int:pk>/', views.display_university, name='display_university'),
    path('student/<int:pk>', views.display_student, name='display_student'),
    path('universities/', views.display_universities_all, name='display_universities_all'),
    path('companies/', views.display_companies_all, name='display_companies_all'),
    path('vacancies/', views.display_vacancies_all, name='display_vacancies_all'),
    path('statistics/', views.display_statistics, name='statistics'),
    path('get_top10competencies_bycompanies/', views.get_top10competencies_bycompanies, name='get_top10competencies_bycompanies'),
    path('get_top10companies_byvacancies/', views.get_top10companies_byvacancies, name='get_top10companies_byvacancies'),
    path('get_top10universities_bystudents/', views.get_top10universities_bystudents, name='get_top10universities_bystudents'),
    path('get_top10subjectsareasvacancies/', views.get_top10subjectsareasvacancies, name='get_top10subjectsareasvacancies'),
    path('profile/get-suitable-vacancies/', views.display_suitablevacancies, name='display_suitablevacancies'),
    path('profile/get-suitable-students/<int:pk>', views.display_suitablestudents, name='display_suitablestudents')
]
