import datetime

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Topic, Course, Student
from .forms import SearchForm, OrderForm, ReviewForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
# def index(request):
#     top_list = Topic.objects.all().order_by('id')[:10]
#     course_list = Course.objects.all().order_by('id')[:5]
#     response = HttpResponse()
#     heading1 = '<p>' + 'List of topics: ' + '</p>'
#     heading2 = '<p>' + 'List of courses' + '</p>'
#     response.write(heading1)
#
#     for topic in top_list:
#         para = '<p>'+ str(topic.id) + ': ' + str(topic) + '</p>'
#         response.write(para)
#
#     sorted_list=sorted(course_list,key= operator.attrgetter('title'),reverse=True)
#     response.write(heading2)
#     for course in sorted_list:
#         para = '<p>' + str(course) + ', Price: ' + str(course.price) + '</p>'
#         response.write(para)
#     return response
#
# def about(request):
#     data = 'This is an E-learning Website! Search our Topics to find all available Courses.'
#     return render(request, 'templates/myapp/about0.html', {'data' : data})
#
# def detail(request, topic_id):
#     topic= Topic.objects.get(id=topic_id)
#     topic= get_object_or_404(Topic, id=topic_id)
#     course_list =Course.objects.filter(topic=topic)
#
#     response = HttpResponse()
#     para= '<p><b>' + str(topic.name).upper() + '<br>' +'Length: '+str(topic.length)+ '</b></p>'
#     response.write(para)
#
#     heading1 = '<p>' + 'List of available courses:' + '</p>'
#     response.write(heading1)
#     for course in course_list:
#         para1= '<p>' + str(course.title) + '</p>'
#         response.write(para1)
#     return response


def index(request):
    username=request.user.username;
    if 'last_login' in request.session:
        last_login=str(request.session['last_login'])
    else:
        return HttpResponse('Your last login was more than one hour ago. Please login again!')
    top_list = Topic.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'top_list': top_list,'last_login':last_login ,'username' : username})

def about(request):
    username = request.user.username
    data = 'This is an E-learning Website! Search our Topics to find all available Courses.'
    if 'about_visits' in request.COOKIES:
        total_visits=int(request.COOKIES['about_visits'])
        total_visits=total_visits+1
    else:
        total_visits=1
    response = render(request, 'myapp/about.html', {'data' : data, 'total_visits': total_visits , 'username' : username})
    response.set_cookie('about_visits',total_visits,max_age=5*60)
    return response

def detail(request, topic_id):
    username = request.user.username
    topic = get_object_or_404(Topic, id=topic_id)
    course_list = Course.objects.filter(topic=topic)
    return render(request, 'myapp/detail.html', {'topic': topic, 'course_list': course_list, 'username' : username})

def findcourses(request):
    username=request.user.username
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            courselist = []
            if length == '':
                courselist=Course.objects.filter(price__lte=max_price)
                return render(request, 'myapp/results.html',
                              {'courselist': courselist, 'name': name, 'username': username})
            else:
                topics = Topic.objects.filter(length=length)
                for top in topics:
                    courselist = courselist + list(top.courses.all())
                return render(request, 'myapp/results.html',
                              {'courselist':courselist, 'name':name, 'username': username})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
    return render(request, 'myapp/findcourses.html', {'form': form, 'username':username})

def place_order(request):
    username = request.user.username
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save()
            student = order.Student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order':order, 'username': username})
        else:
            return render(request, 'myapp/place_order.html', {'form':form, 'username':username})
    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form':form, 'username':username})

def review(request):
    username=request.user.username
    if request.method == 'POST':
        form= ReviewForm(request.POST)
        if form.is_valid():
            rating= form.cleaned_data['rating']
            if(rating<1 or rating>5):
                form.add_error('rating','You must enter a rating between 1 and 5')
                return render(request, 'myapp/review.html', {'form': form, 'username': username})
            review = form.save()
            course_id = review.course.id
            course=Course.objects.get(id=course_id)
            course.num_reviews=course.num_reviews+1
            course.save()
            response = redirect('myapp:index')
            return response
        else:
            return render(request, 'myapp/review.html', {'form': form, 'username': username})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form': form, 'username': username})

# def review(request):
#     username=request.user.username
#     if request.method == 'POST':
#         form= ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             course_id = review.course.id
#             course=Course.objects.get(id=course_id)
#             course.num_reviews=course.num_reviews+1
#             course.save()
#             review.save()
#             response = redirect('myapp:index')
#             return response
#         else:
#             return render(request, 'myapp/review.html', {'form': form, 'username': username})
#     else:
#         form = ReviewForm()
#         return render(request, 'myapp/review.html', {'form': form, 'username': username})

# Import necessary classes and models

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                currentTime=str(datetime.datetime.now().strftime('%H:%M:%S'))
                request.session['last_login']=currentTime
                request.session.set_expiry(60*60)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(('myapp:index')))

def myaccount(request):
    username = request.user.username
    try:
        user = Student.objects.get(username=username)
    except Student.DoesNotExist:
        user=None
    if user:
        firstName=user.first_name
        lastName=user.last_name
        interested_in=Student.objects.filter(username=username).values_list('interested_in__name',flat=True)
        registered_courses=Student.objects.filter(username=username).values_list('registered_courses__title',flat=True)
        return render(request, 'myapp/myaccount.html',
                      {'firstName':firstName, 'lastName':lastName,'registered_courses': registered_courses,
                       'interested_in':interested_in, 'username':username})
    else:
        return HttpResponse('You are not a registered student!')