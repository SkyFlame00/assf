from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout as logout_func, authenticate
from django.db import IntegrityError, transaction
import json
import operator

from .models import *
from .forms import *


def index(request):
    user = request.user
    search_form = SearchForm()
    last5vacs = Vacancy.objects.all()[:5]
    last5companies = Company.objects.all()[:5]

    if request.method == 'POST':

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        search_form = SearchForm(request.POST)

        if username is not None and password is not None:
            user_authenticated = authenticate(username=username, password=password)

            if user_authenticated is not None:
                login(request, user_authenticated)
                return HttpResponseRedirect(request.GET.get('next', '/'))
            else:
                return HttpResponse('Data, you entered, is wrong')



    else:
        pass

    return render(
        request,
        'index.html',
        {
            'user': user,
            'search_form': search_form,
            'last5vacs': last5vacs,
            'last5companies': last5companies
        }
    )


def logout(request):
    logout_func(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def register_university(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        university_form = UniversityForm(request.POST)

        if user_form.is_valid() and university_form.is_valid():
            password = user_form.cleaned_data.get('password')
            user = user_form.save(commit=False)
            user.set_password(password)
            user.user_type = 'unv'
            user.save()

            # The second parameter in get method is a default value
            title = university_form.cleaned_data.get('title')
            city = university_form.cleaned_data.get('city')
            foundation_year = university_form.cleaned_data.get('foundation_year')
            description = university_form.cleaned_data.get('description')
            University.objects.create(user=user, title=title, city=city, foundation_year=foundation_year, description=description, verified=False)

            return HttpResponse('Success!')
    else:
        user_form = UserForm()
        university_form = UniversityForm()

    return render(
        request,
        'main/register_university.html',
        {
            'user_form': user_form,
            'university_form': university_form
        }
    )


def register_company(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        company_form = CompanyForm(request.POST)

        if user_form.is_valid() and company_form.is_valid():
            password = user_form.cleaned_data.get('password')
            user = user_form.save(commit=False)
            user.set_password(password)
            user.user_type = 'com'
            user.save()

            # The second parameter in get method is a default value
            name = company_form.cleaned_data.get('name', '')
            foundation_year = company_form.cleaned_data.get('foundation_year', 0)
            description = company_form.cleaned_data.get('description', '')
            Company.objects.create(user=user, name=name, foundation_year=foundation_year, description=description, verified=False)

            return HttpResponse('Success!')
    else:
        user_form = UserForm()
        company_form = CompanyForm()

    return render(
        request,
        'main/register_company.html',
        {
            'user_form': user_form,
            'company_form': company_form
        }
    )


def register_student(request):
    StudentEducationFormset = formset_factory(StudentEducationForm, extra=1)
    StudentJobFormset = formset_factory(StudentJobForm, extra=1)
    subject_areas_raw = SubjectArea.objects.all()
    subject_areas = []

    for subject_area in subject_areas_raw:
        subject_areas.append({'id': subject_area.id, 'title': subject_area.title})

    StudentAdditionalCompetencyFormset = formset_factory(StudentAdditionalCompetencyForm, extra=0)

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        studenteducation_formset = StudentEducationFormset(request.POST)
        studentjob_formset = StudentJobFormset(request.POST, prefix='job')
        studentadditionalcompetency_formset = StudentAdditionalCompetencyFormset(request.POST, prefix='competency')
        educFormsAmount = len(studenteducation_formset)

        if user_form.is_valid() and student_form.is_valid() and studenteducation_formset.is_valid() and studentjob_formset.is_valid() and studentadditionalcompetency_formset.is_valid():
            password = user_form.cleaned_data.get('password')
            user = user_form.save(commit=False)
            user.set_password(password)
            user.user_type = 'st'
            user.save()

            first_name = student_form.cleaned_data.get('first_name')
            last_name = student_form.cleaned_data.get('last_name')
            patronymic = student_form.cleaned_data.get('patronymic')
            city = student_form.cleaned_data.get('city')

            student = Student.objects.create(user=user, first_name=first_name, last_name=last_name, patronymic=patronymic, city=city)

            studeducs = []
            studjobs = []
            programs = []
            competencies_raw = []

            for studeduc in studenteducation_formset:
                #competencies_raw.append(UniversityProgram.objects.get(pk=int(studeduc.cleaned_data.get('program'))).competencies.all())
                competencies_raw.append(studeduc.cleaned_data.get('program').competencies.all())

                studeducs.append(StudentEducation(
                    student=student,
                    university=studeduc.cleaned_data.get('university'),
                    degree=studeduc.cleaned_data.get('degree'),
                    program=studeduc.cleaned_data.get('program'),
                    year_start=studeduc.cleaned_data.get('year_start'),
                    year_end=studeduc.cleaned_data.get('year_end')
                ))

            competencies_flatten = []

            for competencies_set in competencies_raw:
                for competency in competencies_set:
                    competencies_flatten.append(competency)

            competencies_pre = list(set(competencies_flatten))
            competencies_final = []
            additionalcomps = []

            for form in studentadditionalcompetency_formset:
                additionalcomps.append(Competency(pk=int(form.cleaned_data.get('competency'))))

            competencies_final = competencies_pre + additionalcomps
            competencies_final = list(set(competencies_final))

            studcomps = []

            for competency in competencies_final:
                studcomps.append(StudentCompetency(student=student, competency=competency))

            if len(studentjob_formset) > 0:
                for studjob in studentjob_formset:
                    studjobs.append(StudentJob(
                        student=student,
                        company=studjob.cleaned_data.get('company'),
                        position=studjob.cleaned_data.get('position'),
                        year_start=studjob.cleaned_data.get('year_start'),
                        year_end=studjob.cleaned_data.get('year_end')
                    ))


            try:
                with transaction.atomic():
                    StudentEducation.objects.bulk_create(studeducs)
                    StudentJob.objects.bulk_create(studjobs)
                    StudentCompetency.objects.bulk_create(studcomps)

            except IntegrityError:
                return HttpResponse('An error occured while creating your profile')

            return HttpResponse('Success!')
    else:
        user_form = UserForm()
        student_form = StudentForm()
        studenteducation_formset = StudentEducationFormset()
        studentjob_formset = StudentJobFormset(prefix='job')
        studentadditionalcompetency_formset = StudentAdditionalCompetencyFormset(prefix='competency')
        educFormsAmount = len(studenteducation_formset)

    return render(
        request,
        'main/register_student.html',
        {
            'user_form': user_form,
            'student_form': student_form,
            'studenteducation_formset': studenteducation_formset,
            'studentjob_formset': studentjob_formset,
            'subject_areas': subject_areas,
            'studentadditionalcompetency_formset': studentadditionalcompetency_formset,
            'educFormsAmount': educFormsAmount,
            'tes': len(studentjob_formset)
        }
    )


def profile(request):
    user = request.user
    user_type = None
    data = None

    if user.is_authenticated:
        user_type = user.user_type

        if user_type == 'unv':
            university = University.objects.get(user=user)
            bachelor = list(UniversityProgram.objects.filter(university=university, degree='bac').order_by('-id')[:10])
            magister = list(UniversityProgram.objects.filter(university=university, degree='mag').order_by('-id')[:10])
            programs = list(UniversityProgram.objects.filter(university=university))

            data = {
                'id': university.id,
                'title': university.title,
                'foundation_year': university.foundation_year,
                'description': university.description,
                'city': university.city,
                'verified': university.verified,
                'programs': programs,
                'bachelor': bachelor,
                'magister': magister
            }

            return render(
                request,
                'main/display_university.html',
                {
                    'user_type': user_type,
                    'data': data,
                    'user': user,
                    'university': university
                }
            )

        if user_type == 'st':
            student = Student.objects.get(user=user)
            educations = list(student.studenteducation_set.all())
            jobs = list(student.studentjob_set.all())
            competencies = list(student.studentcompetency_set.all())
            who_verified = []
            for competency in competencies:
                who_verified.append(list(competency.who_verified.all()))

            data = {
                'username': student.user.username,
                'email': student.user.email,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'patronymic': student.patronymic,
                'city': student.city,
                'educations': educations,
                'educationsAmount': len(educations),
                'jobs': jobs,
                'jobsAmount': len(jobs),
                'competencies': competencies,
                'who_verified': who_verified
            }

            return render(
                request,
                'main/display_student.html',
                {
                    'user_type': user_type,
                    'data': data
                }
            )

        if user_type == 'com':
            company = Company.objects.get(user=user)
            vacancies = list(Vacancy.objects.filter(company=company))

            data = {
                'id': company.id,
                'name': company.name,
                'foundation_year': company.foundation_year,
                'description': company.description,
                'verified': company.verified,
                'vacancies': vacancies
            }

            return render(
                request,
                'main/display_company.html',
                {
                    'user_type': user_type,
                    'data': data,
                    'user': user,
                    'company': company
                }
            )
    else:
        return HttpResponse('You are not authenticated')

    return render(
        request,
        'main/profile.html',
        {
            'user_type': user_type,
            'data': data
        }
    )


def add_program(request):
    user = request.user
    addprogramform = AddProgramForm()
    AddCompetencyFieldFormset = formset_factory(AddProgramCompetencyForm)
    data = []
    subject_areas_raw = SubjectArea.objects.all()
    subject_areas = []

    for subject_area in subject_areas_raw:
        subject_areas.append({'id': subject_area.id, 'title': subject_area.title})

    if user.user_type == 'unv':
        university = University.objects.get(user=user)

        if request.method == 'POST':
            addprogramform = AddProgramForm(request.POST)
            addcompetencyfield_formset = AddCompetencyFieldFormset(request.POST, prefix='competency')

            if addprogramform.is_valid() and addcompetencyfield_formset.is_valid():
                title = addprogramform.cleaned_data.get('title')
                description = addprogramform.cleaned_data.get('description')
                degree = addprogramform.cleaned_data.get('degree')

                program = UniversityProgram.objects.create(
                    university=university,
                    title=title,
                    description=description,
                    degree=degree
                )

                for form in addcompetencyfield_formset:
                    data.append(form.cleaned_data.get('competency'))

                program.competencies.add(*data)

                return HttpResponse('Success!')
        else:
            addprogramform = AddProgramForm(initial={'university': university})
            addcompetencyfield_formset = AddCompetencyFieldFormset(prefix='competency')
    else:
        return HttpResponse('You have no permission to access this page')

    return render(
        request,
        'main/add_program.html',
        {
            'addprogramform': addprogramform,
            'addcompetencyfield_formset': addcompetencyfield_formset,
            'subject_areas': subject_areas
        }
    )


def add_vacancy(request):
    user = request.user
    AddVacancyCompetencyFormset = formset_factory(AddVacancyCompetencyForm, extra=0)

    subject_areas_raw = SubjectArea.objects.all()
    subject_areas = []
    
    for subject_area in subject_areas_raw:
        subject_areas.append({'id': subject_area.id, 'title': subject_area.title})

    if user.is_authenticated and user.user_type == 'com':
        if request.method == 'POST':
            addvacancy_form = AddVacancyForm(request.POST)
            addvacancycompetency_formset = AddVacancyCompetencyFormset(request.POST, prefix='competency')

            if addvacancy_form.is_valid() and addvacancycompetency_formset.is_valid():
                cleaned_data = addvacancy_form.cleaned_data
                company = Company.objects.get(user=user)

                vacancy = Vacancy.objects.create(
                    company=company,
                    title=cleaned_data.get('title'),
                    description=cleaned_data.get('description')
                )

                competencies = []

                for form in addvacancycompetency_formset:
                    competencies.append(form.cleaned_data.get('competency'))

                vacancy.competencies.add(*competencies)

                return HttpResponse('Success!')
        else:
            addvacancy_form = AddVacancyForm()
            addvacancycompetency_formset = AddVacancyCompetencyFormset(prefix='competency')
    else:
        return HttpResponse('You are not logged in as a company')

    return render(
        request,
        'main/add_vacancy.html',
        {
            'addvacancy_form': addvacancy_form,
            'addvacancycompetency_formset': addvacancycompetency_formset,
            'subject_areas': subject_areas
        }
    )


def get_subjectarea(request):
    subject_area_id = int(request.GET['subject_area_id'])
    subject_area = SubjectArea.objects.get(id=subject_area_id)
    competencies = subject_area.competency_set.all()
    final_data = {}
    i = 0

    for competency in competencies:
        final_data[i] = {'id': competency.id, 'title': competency.title}
        i += 1

    return HttpResponse(json.dumps(final_data))


def get_universities(request):
    universities = University.objects.all()
    final_data = {}

    i = 0
    for university in universities:
        final_data[i] = {'id': university.id, 'title': university.title}
        i += 1

    return HttpResponse(json.dumps(final_data))


def get_programs(request):
    university_id = int(request.GET['university'])
    degree = request.GET['degree']

    programs = UniversityProgram.objects.all().filter(university=university_id, degree=degree)

    final_data = {}
    i = 0

    for program in programs:
        final_data[i] = {'id': program.id, 'title': program.title}
        i += 1

    return HttpResponse(json.dumps(final_data))


def get_companies(request):
    companies = Company.objects.all()

    final_data = {}

    i = 0
    for company in companies:
        final_data[i] = {'id': company.id, 'name': company.name}
        i += 1

    return HttpResponse(json.dumps(final_data))


def display_program(request, pk):
    program = UniversityProgram.objects.get(pk=pk)

    return render(
        request,
        'main/display_program.html',
        {
            'university': program.university,
            'title': program.title,
            'description': program.description,
            'degree': program.degree,
            'competencies': program.competencies.all(),
            'program': program
        }
    )


def display_programs(request, pk):
    university = University.objects.get(pk=pk)
    programs_raw = UniversityProgram.objects.filter(university=university)
    programs = []

    for program in programs_raw:
        pass

    return render(
        request,
        'main/display_programs.html',
        {
            'university': university,
            'programs': programs_raw
        }
    )


def display_vacancy(request, pk):
    vacancy = Vacancy.objects.get(pk=pk)

    return render(
        request,
        'main/display_vacancy.html',
        {
            'company': vacancy.company,
            'title': vacancy.title,
            'description': vacancy.description,
            'competencies': vacancy.competencies.all()
        }
    )


def display_vacancies(request, pk):
    company = Company.objects.get(pk=pk)
    vacancies = Vacancy.objects.filter(company=company)

    return render(
        request,
        'main/display_vacancies.html',
        {
            'company': company,
            'vacancies': vacancies
        }
    )


def verify_students(request):
    user = request.user
    VerifyStudentFormset = formset_factory(VerifyStudentForm, extra=0)
    data=[]
    final_data=[]

    if user.is_authenticated and user.user_type == 'unv':
        university = University.objects.get(user=user)

        if request.method == 'POST':
            verifystudent_formset = VerifyStudentFormset(request.POST)

            if verifystudent_formset.is_valid():

                for form in verifystudent_formset:
                    StudentEducation.objects.filter(id=form.cleaned_data.get('num')).update(verified=form.cleaned_data.get('verified'))

                # Add or remove competencies verification
                for form in verifystudent_formset:
                    id=form.cleaned_data.get('num')
                    verified=form.cleaned_data.get('verified')

                    unv_comps = list(StudentEducation.objects.get(id=id).program.competencies.all())
                    student = StudentEducation.objects.get(id=id).student
                    st_comps_raw = list(student.studentcompetency_set.all())
                    st_comps = []

                    for st_comp_raw in st_comps_raw:
                        st_comps.append(st_comp_raw.competency)

                    if verified == True:
                        for unv_comp in unv_comps:
                            if unv_comp in st_comps:
                                verificators = list(StudentCompetency.objects.get(competency=unv_comp, student=student).who_verified.all())

                                if user in verificators:
                                    continue
                                else:
                                    StudentCompetency.objects.get(competency=unv_comp, student=student).who_verified.add(user)

                            else:
                                comp = StudentCompetency.objects.create(student=student, competency=unv_comp)
                                comp.who_verified.add(user)
                    else:
                        for unv_comp in unv_comps:
                            if unv_comp in st_comps:
                                verificators = list(StudentCompetency.objects.get(competency=unv_comp, student=student).who_verified.all())

                                if user in verificators:
                                    StudentCompetency.objects.get(competency=unv_comp, student=student).who_verified.remove(user)


                studenteducs = StudentEducation.objects.filter(university=university)
                initial_data = []

                for item in studenteducs:
                    initial_data.append({'num': item.id, 'verified': item.verified})

                verifystudent_formset = VerifyStudentFormset(initial=initial_data)

                final_data = []

                for i in range(len(studenteducs)):
                    final_data.append({
                        'raw': studenteducs[i],
                        'id': studenteducs[i].id,
                        'name': studenteducs[i].student,
                        'program': studenteducs[i].program,
                        'form': verifystudent_formset[i]
                    })

                return render(
                    request,
                    'main/verify_students.html',
                    {
                        'university': university,
                        'verifystudent_formset': verifystudent_formset,
                        'data': final_data,
                        'success': True
                    }
                )
        else:
            studenteducs = StudentEducation.objects.filter(university=university)
            initial_data = []

            for item in studenteducs:
                initial_data.append({'num': item.id, 'verified': item.verified})

            verifystudent_formset = VerifyStudentFormset(initial=initial_data)

            final_data = []

            for i in range(len(studenteducs)):
                final_data.append({
                    'id': studenteducs[i].id,
                    'name': studenteducs[i].student,
                    'program': studenteducs[i].program,
                    'degree': studenteducs[i].degree,
                    'form': verifystudent_formset[i]
                })
    else:
        return HttpResponse('You are not logged in as a university')

    return render(
        request,
        'main/verify_students.html',
        {
            'university': university,
            'verifystudent_formset': verifystudent_formset,
            'data': final_data,
            'new_data': data
        }
    )


def verify_students_jobs(request):
    user = request.user
    VerifyStudentJobFormset = formset_factory(VerifyStudentJobForm, extra=0)
    success = False
    post = []
    final_data = []

    if user.is_authenticated and user.user_type == 'com':
        company = Company.objects.get(user=user)
        studentsjobs = StudentJob.objects.filter(company=company)

        if request.method == 'POST':
            verifystudentjob_formset = VerifyStudentJobFormset(request.POST)
            post = request.POST

            if verifystudentjob_formset.is_valid():
                for form in verifystudentjob_formset:
                    StudentJob.objects.filter(pk=form.cleaned_data.get('num')).update(verified=form.cleaned_data.get('verified'))

                initial_data = []
                final_data = []

                for item in studentsjobs:
                    initial_data.append({'num': item.id, 'verified': item.verified})

                verifystudentjob_formset = VerifyStudentJobFormset(initial=initial_data)

                for i in range(len(studentsjobs)):
                    final_data.append({
                        'id': studentsjobs[i].id,
                        'student_id': studentsjobs[i].student.id,
                        'name': studentsjobs[i].student,
                        'position': studentsjobs[i].position,
                        'year_start': studentsjobs[i].year_start,
                        'year_end': studentsjobs[i].year_end,
                        'form': verifystudentjob_formset[i]
                    })

                success = True
        else:
            initial_data = []
            final_data = []

            for item in studentsjobs:
                initial_data.append({'num': item.id, 'verified': item.verified})

            verifystudentjob_formset = VerifyStudentJobFormset(initial=initial_data)

            for i in range(len(studentsjobs)):
                final_data.append({
                    'id': studentsjobs[i].id,
                    'student_id': studentsjobs[i].student.id,
                    'name': studentsjobs[i].student,
                    'position': studentsjobs[i].position,
                    'year_start': studentsjobs[i].year_start,
                    'year_end': studentsjobs[i].year_end,
                    'form': verifystudentjob_formset[i]
                })
    else:
        return HttpResponse('You are not logged in as a company')

    return render(
        request,
        'main/verify_students_jobs.html',
        {
            'company': company,
            'verifystudentjob_formset': verifystudentjob_formset,
            'data': final_data,
            'success': success,
            'post': post
        }
    )


def verify_student_competencies(request, pk):
    user = request.user
    VerifyStudentCompetenciesFormset = formset_factory(VerifyStudentCompetenciesForm, extra=0)
    data = []
    success = False
    here = 'no'
    post = []

    if user.is_authenticated and user.user_type == 'com':
        student = Student.objects.get(pk=pk)
        competencies = StudentCompetency.objects.filter(student=student)

        if request.method == 'POST':
            verifystudentcompetencies_formset = VerifyStudentCompetenciesFormset(request.POST)
            post = request.POST

            if verifystudentcompetencies_formset.is_valid():
                here = 'yes'
                for form in verifystudentcompetencies_formset:
                    form_id = form.cleaned_data.get('num')

                    if form.cleaned_data.get('verified') == True:
                        if user in list(competencies.filter(pk=form_id)[0].who_verified.all()):
                            continue
                        else:
                            competencies.filter(pk=form_id)[0].who_verified.add(user)
                    else:
                        if user in list(competencies.filter(pk=form_id)[0].who_verified.all()):
                            competencies.filter(pk=form_id)[0].who_verified.remove(user)
                        else:
                            continue

                competencies = StudentCompetency.objects.filter(student=student)
                data = []

                for i in range(len(verifystudentcompetencies_formset)):
                    who_else_verified = []

                    for item in list(competencies[i].who_verified.all()):
                        if item != user:
                            who_else_verified.append(item)

                    data.append({
                        'id': competencies[i].id,
                        'competency': competencies[i].competency,
                        'category': competencies[i].competency.subject_area,
                        'who_else_verified': who_else_verified,
                        'form': verifystudentcompetencies_formset[i]
                    })

                success = True
        else:
            initial_data = []

            for competency in competencies:
                if user in list(competency.who_verified.all()):
                    is_verified = True
                else:
                    is_verified = False

                initial_data.append({
                    'num': competency.id,
                    'verified': is_verified
                })

            verifystudentcompetencies_formset = VerifyStudentCompetenciesFormset(initial=initial_data)
            data = []

            for i in range(len(verifystudentcompetencies_formset)):
                who_else_verified = []

                for item in list(competencies[i].who_verified.all()):
                    if item != user:
                        who_else_verified.append(item)

                data.append({
                    'id': competencies[i].id,
                    'competency': competencies[i].competency,
                    'category': competencies[i].competency.subject_area,
                    'who_else_verified': who_else_verified,
                    'form': verifystudentcompetencies_formset[i],
                    'student': student
                })
    else:
        return HttpResponse('You are not logged in as a company')

    return render(
        request,
        'main/verify_student_competencies.html',
        {
            'student': student,
            'data': data,
            'verifystudentcompetencies_formset': verifystudentcompetencies_formset,
            'success': success,
            'here': here,
            'post': post
        }
    )


def display_company(request, pk):
    company = Company.objects.get(pk=pk)
    vacancies = list(Vacancy.objects.filter(company=company))
    user = request.user

    if user == company.user:
        return redirect('profile')

    data = {
        'id': company.id,
        'name': company.name,
        'foundation_year': company.foundation_year,
        'description': company.description,
        'verified': company.verified,
        'vacancies': vacancies
    }

    return render(
        request,
        'main/display_company.html',
        {
            'data': data,
            'user': user,
            'company': company
        }
    )


def display_university(request, pk):
    university = University.objects.get(pk=pk)
    user = request.user

    if user == university.user:
        return redirect('profile')

    bachelor = list(UniversityProgram.objects.filter(university=university, degree='bac').order_by('-id')[:10])
    magister = list(UniversityProgram.objects.filter(university=university, degree='mag').order_by('-id')[:10])
    programs = list(UniversityProgram.objects.filter(university=university))

    data = {
        'id': university.id,
        'title': university.title,
        'foundation_year': university.foundation_year,
        'description': university.description,
        'city': university.city,
        'verified': university.verified,
        'programs': programs,
        'bachelor': bachelor,
        'magister': magister,
        'bg_src': university.bg_src
    }

    return render(
        request,
        'main/display_university.html',
        {
            'data': data,
            'user': user,
            'university': university
        }
    )


def display_student(request, pk):
    student = Student.objects.get(pk=pk)
    user = request.user

    if user == student.user:
        return redirect('profile')

    educations = list(student.studenteducation_set.all())
    jobs = list(student.studentjob_set.all())
    competencies = list(student.studentcompetency_set.all())
    who_verified = []
    for competency in competencies:
        who_verified.append(list(competency.who_verified.all()))

    data = {
        'username': student.user.username,
        'email': student.user.email,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'patronymic': student.patronymic,
        'city': student.city,
        'educations': educations,
        'educationsAmount': len(educations),
        'jobs': jobs,
        'jobsAmount': len(jobs),
        'competencies': competencies,
        'who_verified': who_verified
    }

    return render(
        request,
        'main/display_student.html',
        {
            'data': data
        }
    )


def display_universities_all(request):
    universities = University.objects.all()

    return render(
        request,
        'main/display/display_universities_all.html',
        {
            'universities': universities
        }
    )


def display_companies_all(request):
    companies = Company.objects.all()

    return render(
        request,
        'main/display/display_companies_all.html',
        {
            'companies': companies
        }
    )


def display_vacancies_all(request):
    vacancies = Vacancy.objects.all()

    return render(
        request,
        'main/display/display_vacancies_all.html',
        {
            'vacancies': vacancies
        }
    )


def display_statistics(request):

    return render(
        request,
        'main/statistics.html',
        {


        }
    )


def get_top10competencies_bycompanies(request):
    vacancies = Vacancy.objects.all()
    competencies = []

    for vacancy in vacancies:
        for competency in vacancy.competencies.all():
            competencies.append(competency)

    competencies_headers = list(set(competencies))

    data_raw = {}
    all = 0

    for header in competencies_headers:
        i = 0

        for competency in competencies:
            if header == competency:
                i += 1

        all += i
        data_raw[header.title] = i

    for item in data_raw:
        data_raw[item] = round((data_raw[item] / all) * 100, 2)

    sorted_d = sorted(data_raw.items(), key=operator.itemgetter(1), reverse=True)[:5]

    return HttpResponse(json.dumps(sorted_d))


def get_top10companies_byvacancies(request):
    companies = Company.objects.all()

    data_raw = {}

    for company in companies:
        data_raw[company.name] = len(list(company.vacancy_set.all()))

    data = {}

    for item in data_raw:
        if data_raw[item] != 0:
            data[item] = data_raw[item]

    sorted_d = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:5]

    return HttpResponse(json.dumps(sorted_d))


def get_top10universities_bystudents(request):
    universities = University.objects.all()
    data_raw = {}
    data = {}

    for university in universities:
        studenteducations = StudentEducation.objects.filter(university=university)
        students = []

        for studenteducation in studenteducations:
            students.append(studenteducation.student)

        students = list(set(students))
        data_raw[university.title] = len(students)

    for item in data_raw:
        if data_raw[item] != 0:
            data[item] = data_raw[item]

    data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:5]

    return HttpResponse(json.dumps(data))


def get_top10subjectsareasvacancies(request):
    vacancies = list(Vacancy.objects.all())
    subject_areas = list(SubjectAreaVacancies.objects.all())
    subject_areas_total = []

    for vacancy in vacancies:
        subject_areas_total.append(vacancy.subject_area)

    data = {}

    for subject_area in subject_areas:
        i = 0

        for item in subject_areas_total:
            if subject_area == item:
                i += 1

        data[subject_area.title] = i

    data = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:5]

    return HttpResponse(json.dumps(data))


def display_suitablevacancies(request):
    user = request.user
    vacancies = Vacancy.objects.all()
    student = Student.objects.get(user=user)
    student_competencies_raw = list(StudentCompetency.objects.filter(student=student))
    student_competencies = []

    for competency in student_competencies_raw:
        student_competencies.append(competency.competency)

    data = []

    for vacancy in vacancies:
        vacancy_competencies = list(vacancy.competencies.all())
        vacancy_competencies_amount = len(vacancy_competencies)
        have = []
        not_have = []
        have_amount = 0

        for vacancy_competency in vacancy_competencies:
            if vacancy_competency in student_competencies:
                have.append(vacancy_competency)
                have_amount += 1
            else:
                not_have.append(vacancy_competency)

        data.append({
            'vacancy': vacancy,
            'overlap': round((have_amount / vacancy_competencies_amount) * 100),
            'have': have,
            'not_have': not_have
        })

    data_final = sorted(data, key=operator.itemgetter('overlap'), reverse=True)

    return render(
        request,
        'main/display/display_suitablevacancies.html',
        {
            'data': data_final,
            'student': student
        }
    )


def display_suitablestudents(request, pk):
    vacancy = Vacancy.objects.get(pk=pk)
    vacancy_competencies = list(vacancy.competencies.all())
    vacancy_competencies_amount = len(vacancy_competencies)
    students = list(Student.objects.all())
    data_raw = []

    for student in students:
        student_competencies_raw = StudentCompetency.objects.filter(student=student)
        student_competencies = []

        for studentcompetency in student_competencies_raw:
            student_competencies.append(studentcompetency.competency)

        have = []
        not_have = []
        have_amount = 0

        for competency in vacancy_competencies:
            if competency in student_competencies:
                have.append(competency)
                have_amount += 1
            else:
                not_have.append(competency)

        data_raw.append({
            'student': student,
            'overlap': round((have_amount / vacancy_competencies_amount) * 100),
            'have': have,
            'not_have': not_have
        })

        data = sorted(data_raw, key=operator.itemgetter('overlap'), reverse=True)

    return render(
        request,
        'main/display/display_suitablestudents.html',
        {
            'data': data,
            'student': student,
            'vacancy': vacancy
        }
    )
