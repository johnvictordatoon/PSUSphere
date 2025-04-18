"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from studentorg.views import HomePageView, OrganizationList, OrganizationCreateView, OrganizationUpdateView, OrganizationDeleteView
from studentorg import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePageView.as_view(), name='home'),
    path('organization_list', OrganizationList.as_view(), name='organization-list'),
    path('organization_list/add', OrganizationCreateView.as_view(), name='organization-add'),
    path('organization_list/<pk>', OrganizationUpdateView.as_view(), name='organization-update'),
    path('organization_list/<pk>/delete', OrganizationDeleteView.as_view(), name='organization-delete'),
    path('orgmember_list', views.OrgMemberList.as_view(), name='orgmember-list'),
    path('orgmember_list/add', views.OrgMemberCreateView.as_view(), name='orgmember-add'),
    path('orgmember_list/<pk>', views.OrgMemberUpdateView.as_view(), name='orgmember-update'),
    path('orgmember_list/<pk>/delete', views.OrgMemberDeleteView.as_view(), name='orgmember-delete'),
    path('student_list/', views.StudentListView.as_view(), name='student-list'),
    path('student_list/add/', views.StudentCreateView.as_view(), name='student-add'),
    path('student_list/<pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('student_list/<pk>/delete/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('college_list/', views.CollegeListView.as_view(), name='college-list'),
    path('college_list/add/', views.CollegeCreateView.as_view(), name='college-add'),
    path('college_list/<pk>/', views.CollegeUpdateView.as_view(), name='college-update'),
    path('college_list/<pk>/delete/', views.CollegeDeleteView.as_view(), name='college-delete'),
    path('program_list/', views.ProgramListView.as_view(), name='program-list'),
    path('program_list/add/', views.ProgramCreateView.as_view(), name='program-add'),
    path('program_list/<pk>/', views.ProgramUpdateView.as_view(), name='program-update'),
    path('program_list/<pk>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]