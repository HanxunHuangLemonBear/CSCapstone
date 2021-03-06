"""
UniversitiesApp Views

Created by Jacob Dunbar on 11/5/2016.
"""
from django.shortcuts import render
from django.db.models import Max
from . import models
from . import forms
import datetime


def isProfessor():
    latest_login = models.MyUser.objects.all().aggregate(Max('last_login'))
    dt = latest_login['last_login__max']
    date_and_time = str(dt)[0:26]
    max_user = models.MyUser.objects.filter(last_login=date_and_time)
    return max_user[0].is_professor


def getUniversities(request):
    if request.user.is_authenticated():
        universities_list = models.University.objects.all()
        context = {
            'universities' : universities_list,
        }
        return render(request, 'universities.html', context)
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        is_member = in_university.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'userIsMember': is_member,
        }
        if request.user.is_professor:
            return render(request, 'university.html', context)
        else:
            return render(request, 'universityStudent.html', context)

    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityForm(request):
    if request.user.is_authenticated():
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getUniversityFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            form = forms.UniversityForm(request.POST, request.FILES)
            if form.is_valid():
                if models.University.objects.filter(name__exact=form.cleaned_data['name']).exists():
                    return render(request, 'universityform.html', {'error' : 'Error: That university name already exists!'})
                new_university = models.University(name=form.cleaned_data['name'],
                                             photo=request.FILES['photo'],
                                             description=form.cleaned_data['description'],
                                             website=form.cleaned_data['website'])
                new_university.save()
                context = {
                    'name' : form.cleaned_data['name'],
                }
                return render(request, 'universityformsuccess.html', context)
            else:
                return render(request, 'universityform.html', {'error' : 'Error: Photo upload failed!'})
        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    # render error page if user is not logged in
    return render(request, 'autherror.html')

def getAddStudentFormSuccess(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            formU = forms.UniForm(request.POST, request.FILES)

            if formU.is_valid():
                in_name = formU.cleaned_data['name']
                in_user = models.MyUser.objects.get(email__exact=in_name)

                in_university_name = formU.cleaned_data['univName']
                in_university = models.University.objects.get(name__exact=in_university_name)

                in_course_tag = formU.cleaned_data['cName']
                in_course = in_university.course_set.get(tag__exact=in_course_tag)

                in_course.members.add(in_user)
                in_course.save();
                in_user.course_set.add(in_course)
                in_user.save()

                context = {
                    'university' : in_university,
                    'course' : in_course,
                    'userInCourse': True,
                }

                return render(request, 'course.html', context)
            else:
                print("SOMETHING'S WRONG")

        else:
            form = forms.UniversityForm()
        return render(request, 'universityform.html')
    return render(request, 'autherror.html')

def joinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.add(request.user)
        in_university.save();
        request.user.university_set.add(in_university)
        request.user.university_name = in_university
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': True,
        }
        if (request.user.is_professor):
            return render(request, 'university.html', context)
        else:
            return render(request, 'universityStudent.html', context)
    return render(request, 'autherror.html')

def unjoinUniversity(request):
    if request.user.is_authenticated():
        in_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_name)
        in_university.members.remove(request.user)
        in_university.save();
        request.user.university_set.remove(in_university)
        request.user.university_name = None
        request.user.save()
        context = {
            'university' : in_university,
            'userIsMember': False,
        }
        if (request.user.is_professor):
            return render(request, 'university.html', context)
        else:
            return render(request, 'universityStudent.html', context)
    return render(request, 'autherror.html')

def getCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_course.members.filter(email__exact=request.user.email)
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse' : is_member,
            }
        if request.user.is_professor:
            return render(request, 'course.html', context)
        else:
            return render(request, 'courseStudent.html', context)
    return render(request, 'autherror.html')

def courseForm(request):
	if request.user.is_authenticated():
		in_university_name = request.GET.get('name', 'None')
		in_university = models.University.objects.get(name__exact=in_university_name)
		context = {
			'university': in_university,
		}
		return render(request, 'courseform.html', context)
    # render error page if user is not logged in
	return render(request, 'autherror.html')

def addCourse(request):
	if request.user.is_authenticated():
		if request.method == 'POST':
			form = forms.CourseForm(request.POST)
			if form.is_valid():
				in_university_name = request.GET.get('name', 'None')
				in_university = models.University.objects.get(name__exact=in_university_name)
				if in_university.course_set.filter(tag__exact=form.cleaned_data['tag']).exists():
					return render(request, 'courseform.html', {'error' : 'Error: That course tag already exists at this university!'})
				new_course = models.Course(tag=form.cleaned_data['tag'],
										   name=form.cleaned_data['name'],
										   description=form.cleaned_data['description'],
										   university=in_university)
				new_course.save()
				in_university.course_set.add(new_course)
				is_member = in_university.members.filter(email__exact=request.user.email)
				context = {
					'university' : in_university,
					'userIsMember': is_member,
				}
				return render(request, 'university.html', context)
			else:
				return render(request, 'courseform.html', {'error' : 'Undefined Error!'})
		else:
			form = forms.CourseForm()
			return render(request, 'courseform.html')
		# render error page if user is not logged in
	return render(request, 'autherror.html')

def addStudentForm(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_name = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_name)
        context = {
            'university' : in_university,
            'course' : in_course,
        }
        return render(request, 'addStudentForm.html', context)
    return render(request, 'autherror.html')

def removeCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        is_member = in_university.members.filter(email__exact=request.user.email)
        print(request.user.email)
        print(request.user.is_professor)
        print(request.user.is_student)
        context = {
			'university' : in_university,
			'userIsMember' : is_member,
		}
        if not request.user.is_professor:
            context = {
			'university' : in_university,
			'userIsMember' : is_member,
                        'user_error' : 'Only Professors can remove projects',
	            }
        else:
            in_course.delete()

            if request.user.is_professor:
                return render(request, 'university.html', context)
            else:
                return render(request, 'universityStudent.html', context)

	# render error page if user is not logged in
    return render(request, 'autherror.html')

def joinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.add(request.user)
        in_course.save();
        request.user.course_set.add(in_course)
        request.user.save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            }

        if request.user.is_professor:
            return render(request, 'course.html', context)
        else:
            return render(request, 'courseStudent.html', context)
    return render(request, 'autherror.html')

def unjoinCourseTeach(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_student = request.GET.get('me', 'None')
        in_student = in_student.split( );
        student = models.MyUser.objects.filter(first_name=in_student[0])
        in_course.members.remove(student[0])
        in_course.save();
        student[0].course_set.remove(in_course)
        student[0].save()
        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': True,
            }
        if request.user.is_professor:
            return render(request, 'course.html', context)
        else:
            return render(request, 'courseStudent.html', context)
    return render(request, 'autherror.html')

def unjoinCourse(request):
    if request.user.is_authenticated():
        in_university_name = request.GET.get('name', 'None')
        in_university = models.University.objects.get(name__exact=in_university_name)
        in_course_tag = request.GET.get('course', 'None')
        in_course = in_university.course_set.get(tag__exact=in_course_tag)
        in_course.members.remove(request.user)
        in_course.save();
        request.user.course_set.remove(in_course)
        request.user.save()

        context = {
            'university' : in_university,
            'course' : in_course,
            'userInCourse': False,
            }

        if request.user.is_professor:
            return render(request, 'course.html', context)
        else:
            return render(request, 'courseStudent.html', context)
    return render(request, 'autherror.html')
