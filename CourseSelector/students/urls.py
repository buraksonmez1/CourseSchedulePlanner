from django.contrib.auth.views import LogoutView
from django.urls import path

from students.views import (

    register,
    home,
    about,
    login_view,
    update,
)

urlpatterns = [
    path('', home, name='student-home'),
    path('about/', about, name='student-about'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update/',update, name='update'),

]
