import django.http
from django.shortcuts import render
from django.views.generic import View

from schedule.models import  Schedule
from students.models import Courses
class HomeView(View):

    def get(self, request):
        schedule_display=Schedule.objects.all()
        qs = Courses.objects.all()
        context = {}
        context['courses'] = qs
        context['schedule']=schedule_display

        return render(self.request, 'schedule.html', context)


class scheduleUpdateView(View):

    def post(self,request):
        name = request.POST.get('name', None)
        schedule_qs=Courses.objects.filter(name=name)


        if schedule_qs.exists():

             item = schedule_qs.first()
             print("cse202",item.date)
             # CONVERT DATE FOR SCHEDULE
             a = self.convert_course_date(item.date)
             print("converted date:", a)
            
             return django.http.JsonResponse({'name':item.name, 'place_in_schedule':a})




    def convert_course_date(self,date):

        test = date.split(" ", 1)
        a = test[0]
        b = test[1]
        g = list(map(str, a))
        i = 0
        while i < len(g)-1:
            if g[i] == 'T' and g[i + 1] == 'h':
                g[i] = g[i] + g[i + 1]
                g.pop(i + 1)
            else:
                i += 1

        schedule_place = ''
        for i in range(0, len(g)):
            schedule_place = schedule_place + g[i] + b[i]

        return schedule_place

class update_schedule(View):

    def get(self, request):
        schedule_display=Schedule.objects.all()
        qs = Courses.objects.all()
        context = {}
        context['courses'] = qs
        context['schedule']=schedule_display
        return render(self.request, 'schedule.html', context)

