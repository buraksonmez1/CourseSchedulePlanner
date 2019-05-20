from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from lxml import html
from django.contrib.auth.hashers import check_password
from django.views.generic import (
    FormView,
    CreateView,
    ListView,
    UpdateView,
)
from .forms import  RegisterForm, LoginForm
from .models import Courses, AllOpenCourses, OpenCoursesForYou, update_user_data

User = get_user_model()

def home(request):

    return render(request, 'students/student.html')

@login_required(login_url='login')
def about(request):
    user = request.user
    #AllOpenCourses.objects.all().delete()
    #User.objects.all().delete()
    AllOpenCourses.opencoursescreate() #for creating the database table of all open courses.
    #requesties()
    opens = OpenCoursesForYou.objects.filter(student=user)
    fdeps = []
    open_F_electives = OpenCoursesForYou.objects.filter(student=user, grade='F').exclude(elective=None).values().distinct()
    for ops in open_F_electives:
        if ops["elective"] not in fdeps:
            fdeps.append(ops["elective"])
    print(fdeps)

    deps = []
    open_electives = OpenCoursesForYou.objects.filter(student=user).exclude(elective=None).values().distinct()
    for ops in open_electives:
        if ops["elective"] not in deps:
            deps.append(ops["elective"])
    deps = [i for i in deps if i not in fdeps]
    print(deps)




    courses = Courses.objects.filter(student=user, grade__contains='F')|Courses.objects.filter(student=user, grade=None)
    st_info = [
        {
         'student_no'    : user.username,
         'gpa'           : user.gpa,
         'name'          : user.name,
         'reg_date'      : user.reg_date,
         'faculty'       : user.faculty,
         'department'    : user.department,
         'major'         : user.major,
         'minor'         : user.minor,
         'd_major'       : user.d_major,
         'no_of_sem'     : user.no_of_sem,
         'totalcredit'   : user.totalcredit,
         'givencredit'   : user.givencredit,
         'fcredits'      : user.fcredits,
         'remaining'     : (user.totalcredit-user.givencredit)
         }]
    context = {
        'st_info': st_info,
        'courses'  : courses,
        'opens'  : opens,
        'fdeps' : fdeps,
        'deps' : deps,
    }
    return render(request, 'students/about.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            pw = form.cleaned_data['password1']
            login(request, new_user)
            update_user_data(new_user, pw)
            return HttpResponseRedirect('/about/')
    else:
        form = RegisterForm()
    return render(request, 'students/upload.html', {'form': form})

@login_required(login_url='login')
def update(request):
    user = request.user
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if user.username==form.cleaned_data['username']:
                if check_password(request.POST['password'], user.password):
                    pw = form.cleaned_data['password']
                    update_user_data(user, pw)
                    return HttpResponseRedirect('/about/')
                else:
                    messages.info(request,'wrong password')
                    return render(request, 'students/update.html', {'form': form})
            else:
                messages.info(request,'wrong username')
                print('wrong username')
                return render(request, 'students/update.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'students/update.html', {'form': form})

def login_view(request):
    if request.method =='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password'],
                                    )
            if new_user is not None:
                login(request, new_user)
                return HttpResponseRedirect('/about/')
            else:
                messages.info(request,'wrong credidentals')
                return render(request, 'students/login.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'students/login.html', {'form':form})

def logout(request):
    if request.method=='POST':
        logout(request)
        return HttpResponseRedirect('/login/')


def requesties():
    alops = AllOpenCourses.objects.all().values()

    transcript = open("students/BME.html",'r',encoding='utf-8')
    tree = html.fromstring(transcript.read())
    tr_elements = tree.xpath('//tr')
    bmepreq = []
    for i in range(2,len(tr_elements)-1):
        list = []
        list.append(tr_elements[i][0].text_content().replace(' ','').replace('\n\t\t\t\t\n\t\t\t\t',''))
        if tr_elements[i][4].text_content().strip()=='Öğretim üyesi izni ile' or tr_elements[i][4].text_content().strip()=='Bölüm izni ile':
            list.append('ONAY')
        elif 've' in tr_elements[i][4].text_content() and 'veya' not in tr_elements[i][4].text_content():
            listve = tr_elements[i][4].text_content().split('ve')
            for i in listve:
                list.append(i.replace('\n\t\t\t\t\n\t\t\t\t',''))
        else:
            list.append(tr_elements[i][4].text_content().replace('\n\t\t\t\t\n\t\t\t\t',''))
        bmepreq.append(list)
    asd = bmepreq
    transcript = open("students/EE.html",'r',encoding='utf-8')
    tree = html.fromstring(transcript.read())
    tr_elements = tree.xpath('//tr')
    bmepreq = []
    for i in range(2,len(tr_elements)-1):
        list = []
        list.append(tr_elements[i][0].text_content().replace(' ','').replace('\n\t\t\t\t\n\t\t\t\t',''))
        if tr_elements[i][4].text_content().strip()=='Öğretim üyesi izni ile' or tr_elements[i][4].text_content().strip()=='Bölüm izni ile':
            list.append('ONAY')
        elif 've' in tr_elements[i][4].text_content() and 'veya' not in tr_elements[i][4].text_content():
            listve = tr_elements[i][4].text_content().split('ve')
            for i in listve:
                list.append(i.replace('\n\t\t\t\t\n\t\t\t\t',''))
        else:
            list.append(tr_elements[i][4].text_content().replace('\n\t\t\t\t\n\t\t\t\t',''))
        bmepreq.append(list)
    qwe = asd + bmepreq
    for all in alops:
        for item in qwe:
            if all["short_name"]==item[0]:
                deneme = ''
                for i in range(1,len(item)):
                    deneme += item[i].replace(' ','')
                if 'Eşkoşul:' in deneme:
                    deneme = deneme.split('Eşkoşul:')
                print(item[0], deneme)
