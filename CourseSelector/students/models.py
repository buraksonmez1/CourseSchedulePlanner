from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from lxml import html
from datetime import datetime
import requests
import random

class UserManager(BaseUserManager):

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given, username, and password.
        """
        if not username:
            raise ValueError('The username can not be null')
        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username        = models.CharField(max_length=100, unique=True)
    name            = models.CharField(max_length=100, null=True, blank=True)
    gpa             = models.FloatField(null=True, blank=True, default=2.0)
    reg_date        = models.CharField(max_length=100, null=True, blank=True)
    reg_date_year   = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    faculty         = models.CharField(max_length=100, null=True, blank=True)
    department      = models.CharField(max_length=100, null=True, blank=True)
    major           = models.CharField(max_length=100, null=True, blank=True)
    minor           = models.CharField(max_length=100, null=True, blank=True)
    d_major         = models.CharField(max_length=100, null=True, blank=True)
    no_of_sem       = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    totalcredit     = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    givencredit     = models.PositiveSmallIntegerField(null=True, blank=True, default=1)
    fcredits        = models.PositiveSmallIntegerField(null=True, blank=True, default=1)

    is_active	 	 = models.BooleanField(('Active Status'),
                                            default=True,
                                            help_text=(
                                                'Designates whether this user account should be considered active.'
                                                ' Set this flag to False instead of deleting accounts.'
                                            ))

    is_staff	 	 = models.BooleanField(('Staff Status'),
                                            default=False,
                                            help_text=(
                                                'Designates whether this user can access the admin site.'
                                            ))

    is_superuser 	 = models.BooleanField(('Super User Status'),
                                             default=False,
                                             help_text=(
                                                'Designates that this user has all permissions'
                                                ' without explicitly assigning them.'
                                             ))
    objects = UserManager()
    USERNAME_FIELD 	 = 'username'

    def __str__(self):
        return self.username

class Courses(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    short_name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=100)
    coursecode = models.CharField(max_length=100, null=True)
    credit = models.PositiveSmallIntegerField(null=True)
    grade = models.CharField(max_length=5, null=True)

    def __str__(self):
        return self.student.username

class OpenCourses(models.Model):
    short_name = models.CharField(max_length=10)
    section = models.CharField(max_length=10,null=True)
    long_name = models.CharField(max_length=150)
    credit = models.CharField(max_length=10, null=True)
    instructor = models.CharField(max_length=100, null=True)
    schedule = models.CharField(max_length=10)
    room = models.CharField(max_length=100)
    campus = models.CharField(max_length=20)
    prereq = models.CharField(max_length=10, null=True, default='girilmemis')
    coreq = models.CharField(max_length=10, null=True, default='girilmemis')

    class Meta:
        abstract = True

class AllOpenCourses(OpenCourses):


    def opencoursescreate():#need to fill all open courses table. Only for initiation
        transcript = open("students/open.html",'r',encoding='latin-1')
        tree = html.fromstring(transcript.read())
        tr_elements = tree.xpath('//tr')
        if AllOpenCourses.objects.count()==0:
            print('getting all open courses from open.html')
            for i in range(6,len(tr_elements)):
                    obj = AllOpenCourses(

                    short_name      = tr_elements[i][0].text_content().split('.')[0],
                    section         = tr_elements[i][0].text_content().split('.')[1],
                    long_name       = tr_elements[i][1].text_content(),
                    credit          = tr_elements[i][3].text_content(),
                    instructor      = tr_elements[i][4].text_content(),
                    schedule        = tr_elements[i][5].text_content(),
                    room            = tr_elements[i][6].text_content(),
                    campus          = tr_elements[i][7].text_content()
                    )
                    obj.save()

    def __str__(self):
        return self.short_name+" "+self.section

class OpenCoursesForYou(OpenCourses):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    grade = models.CharField(max_length=5, null=True, default=None)
    elective = models.CharField(max_length=25, null=True, default=None)

    def __str__(self):
        return self.student.username+" "+self.short_name


def update_user_data(user, pw):

    urllist = ['https://campus1.isikun.edu.tr/','https://campus2.isikun.edu.tr/',\
    'https://campus3.isikun.edu.tr/','https://campus4.isikun.edu.tr/',\
    'https://campus5.isikun.edu.tr/','https://campus6.isikun.edu.tr/',\
    'https://campus7.isikun.edu.tr/','https://campus8.isikun.edu.tr/',\
    'https://campus9.isikun.edu.tr/','https://campus10.isikun.edu.tr/']
    url = urllist[random.randint(0,len(urllist)-1)]
    print(url)
    payload = {
    	'id': user.username,
    	'pass': pw
    }
    print(payload)
    with requests.Session() as s:
        loginurl = url + 'checkpass.asp?'
        try:
            p = s.post(loginurl, data=payload)
        except requests.exceptions.RequestException as e:
            print (e)
            return
        tree = html.fromstring(p.content)
        tr_elements = tree.xpath('//tr')
        if 'Incorrect ID or Password' in tree.text_content():
            print('Incorrect ID or Password')
        elif 'Your account has been disabled' in tree.text_content():
            print('Your account has been disabled')
        else:
            ccrurl = url + 'ccr.asp'
            transcripturl = url +'transcript.asp'
            print('ccr :' ,ccrurl)
            print('transcript :' ,transcripturl)
            ccr = s.get(ccrurl)                        #s.get('https://campus1.isikun.edu.tr/update_ccr.asp')
            transcript = s.get(transcripturl)          #s.get('https://campus1.isikun.edu.tr/update_transcript.asp')
            get_transcript(user, transcript)
            electives_not_finished = get_ccr(user, ccr)
            sublist(user, electives_not_finished, url, s)

def get_transcript(user, transcript):

    print('Transcripting..')
    tree = html.fromstring(transcript.content)
    tr_elements = tree.xpath('//tr')
    user.name = tr_elements[3][1].text_content()
    user.reg_date = tr_elements[2][3].text_content().replace(u'\xa0', u' ').replace('.',"/")
    rdy = user.reg_date.split('/')
    user.reg_date_year = rdy[2]
    user.faculty = tr_elements[5][1].text_content()
    user.department = tr_elements[6][1].text_content()
    user.major = tr_elements[7][1].text_content()
    user.d_major = tr_elements[3][3].text_content()
    user.minor = tr_elements[4][3].text_content()
    user.no_of_sem = tr_elements[9][1].text_content()
    user.gpa = float(tr_elements[len(tr_elements)-5][4].text_content().replace(',',"."))
    user.save()

def get_ccr(user, ccr):

    print('ccring..')
    tree                    = html.fromstring(ccr.content)
    tr_elements             = tree.xpath('//tr')
    totalcredit             = 0
    givencredit             = 0
    fcredits                = 0
    mustbetaken             = []
    electives_not_finished  = []
    Courses.objects.filter(student=user).delete()

    for i in range(5,len(tr_elements)):
        if('SEMESTER' not in tr_elements[i][0].text_content() and 'Out of Curriculum Courses' not in tr_elements[i][0].text_content()):
            str = tr_elements[i][3].text_content().split()
            totalcredit += int(tr_elements[i][2].text_content())
            if len(str)>0 and str[len(str)-2]!='F':
                obj = Courses(id=None, student=user, short_name= str[len(str)-1].replace('(','').replace(')',''), \
                coursecode=tr_elements[i][0].text_content(), long_name=tr_elements[i][1].text_content(), \
                credit = int(tr_elements[i][2].text_content()), grade=str[len(str)-2])
                obj.save()
                givencredit += int(tr_elements[i][2].text_content())
            elif len(str)>0 and str[len(str)-2]=='F':
                obj = Courses(id=None, student=user, short_name= str[len(str)-1].replace('(','').replace(')',''), \
                coursecode=tr_elements[i][0].text_content(), long_name=tr_elements[i][1].text_content(), \
                credit = int(tr_elements[i][2].text_content()), grade=str[len(str)-2])
                obj.save()
                fcredits += int(tr_elements[i][2].text_content())
                mustbetaken.append(tr_elements[i][0].text_content())
            else:
                obj = Courses(id=None, student=user, short_name=tr_elements[i][0].text_content(), \
                coursecode=tr_elements[i][0].text_content(), long_name=tr_elements[i][1].text_content(), \
                credit = int(tr_elements[i][2].text_content()), grade=None)
                obj.save()
                mustbetaken.append(tr_elements[i][0].text_content())

    for i in range(5,len(tr_elements)):
        if('SEMESTER' not in tr_elements[i][0].text_content() and 'Out of Curriculum Courses' not in tr_elements[i][0].text_content()):
            if(tr_elements[i][1].text_content().split()[len(tr_elements[i][1].text_content().split())-1] == 'Elective'\
            and tr_elements[i][0].text_content() in mustbetaken):
                electives_not_finished.append(tr_elements[i][0].text_content())

    user.totalcredit = totalcredit
    user.givencredit = givencredit
    user.fcredits    = fcredits
    user.save()
    return electives_not_finished

def sublist(user, electives_not_finished, url, s):

    sublist_link = url + 'substitution.asp?coursecode=ders&stuid=student_no'
    sublist_link = sublist_link.replace('student_no',user.username)
    OpenCoursesForYou.objects.filter(student=user).delete()

    for item in electives_not_finished:#THIS IS FOR F OR NOT TAKEN ELECTIVE COURSES
        print('sublisting to',item)
        sublist_link = sublist_link.replace('ders',item)
        print(sublist_link)
        sublist = s.get(sublist_link)
        sublist_link = sublist_link.replace(item,'ders')
        tree = html.fromstring(sublist.content)
        tr_elements = tree.xpath('//tr')
        for i in range(4,len(tr_elements)):
            if(tr_elements[i][2].text_content()=='OPEN'):
                allopens = AllOpenCourses.objects.filter(short_name=tr_elements[i][0].text_content()).values()
                for i in allopens:
                    if not (OpenCoursesForYou.objects.filter(student=user, short_name=i["short_name"], section=i["section"], elective=item).exists()):
                        obj = OpenCoursesForYou(
                        student         = user,
                        short_name      = i["short_name"],
                        section         = i["section"],
                        long_name       = i["long_name"],
                        credit          = i["credit"],
                        instructor      = i["instructor"],
                        schedule        = i["schedule"],
                        room            = i["room"],
                        campus          = i["campus"],
                        elective        = item,
                        )
                        if Courses.objects.filter(student=user, short_name=i["short_name"], coursecode=item).exists():
                            obj.grade   = Courses.objects.get(student=user, short_name=i["short_name"]).grade
                        obj.save()

    #THIS IS FOR F AND DD-DC COURSES
    cantake = Courses.objects.filter(student=user, grade__contains='D')|Courses.objects.filter(student=user, grade=None)|Courses.objects.filter(student=user, grade='F')
    cantakeshortnames = cantake.values('short_name')
    for i in cantakeshortnames:
        allopens = AllOpenCourses.objects.filter(short_name=i['short_name']).values()
        if allopens.exists():
            for i in allopens:
                if not (OpenCoursesForYou.objects.filter(student=user, short_name=i["short_name"], section=i["section"]).exists()):
                    obj = OpenCoursesForYou(
                    student         = user,
                    short_name      = i["short_name"],
                    section         = i["section"],
                    long_name       = i["long_name"],
                    credit          = i["credit"],
                    instructor      = i["instructor"],
                    schedule        = i["schedule"],
                    room            = i["room"],
                    campus          = i["campus"],
                    grade           = Courses.objects.get(student=user, short_name=i["short_name"]).grade
                    )
                    obj.save()
