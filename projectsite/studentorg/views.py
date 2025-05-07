from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from studentorg.models import Organization, OrgMember, Student, College, Program, Boat
from studentorg.forms import OrganizationForm, OrgMemberForm, StudentForm, CollegeForm, ProgramForm
from django.urls import reverse_lazy
from typing import Any
from django.db import connection
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

@method_decorator(login_required, name='dispatch')

class HomePageView(ListView):
    model = Organization
    context_object_name = 'home'
    template_name = "chart.html"

class ChartView(TemplateView):
    template_name = 'chart.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    def get_queryset(self, *args, **kwargs):
        pass

def BarChartStudentEnrollment(request):
    query = """
        SELECT 
            org.name, 
            COUNT(om.id) as total
        FROM 
            studentorg_organization org
        LEFT JOIN 
            studentorg_orgmember om 
            ON om.organization_id = org.id
        GROUP BY 
            org.name
        ORDER BY 
            org.name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    result = {}
    for row in rows:
        organization = row[0]
        total = row[1]
        result[organization] = total

    return JsonResponse(result)

def PieChartStudentProgram(request):
    query = """
        SELECT 
            prog.prog_name, 
            COUNT(s.id) as total
        FROM 
            studentorg_program prog
        LEFT JOIN 
            studentorg_student s 
            ON s.program_id = prog.id
        GROUP BY 
            prog.prog_name
        ORDER BY 
            prog.prog_name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    result = {}
    for row in rows:
        program = row[0]
        total = row[1]
        result[program] = total

    return JsonResponse(result)

def LineChartMonthlyEnrollment(request):
    query = """
        SELECT 
            org.name,
            strftime('%m', om.date_joined) AS month,
            COUNT(om.id) AS total
        FROM 
            studentorg_organization org
        LEFT JOIN 
            studentorg_orgmember om ON om.organization_id = org.id
        GROUP BY 
            org.name, month
        ORDER BY 
            org.name, month;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Prepare data: {org: {month: count, ...}, ...}
    orgs = {}
    months = [str(i).zfill(2) for i in range(1, 13)]
    for row in rows:
        org = row[0]
        month = row[1] if row[1] else '01'
        total = row[2]
        if org not in orgs:
            orgs[org] = {m: 0 for m in months}
        orgs[org][month] = total

    # Ensure all organizations are present
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM studentorg_organization")
        all_orgs = [row[0] for row in cursor.fetchall()]
    for org in all_orgs:
        if org not in orgs:
            orgs[org] = {m: 0 for m in months}

    # Sort months
    for org in orgs:
        orgs[org] = [orgs[org][m] for m in months]

    return JsonResponse({
        "months": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "data": orgs
    })

def DoughnutChartStudentCollege(request):
    query = """
        SELECT 
            c.college_name, 
            COUNT(s.id) as total
        FROM 
            studentorg_college c
        LEFT JOIN 
            studentorg_program p ON p.college_id = c.id
        LEFT JOIN 
            studentorg_student s ON s.program_id = p.id
        GROUP BY 
            c.college_name
        ORDER BY 
            c.college_name;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        
    result = {}
    for row in rows:
        college = row[0]
        total = row[1]
        result[college] = total

    return JsonResponse(result)

def BubbleChartTopPrograms(request):
    query = """
        SELECT 
            prog.prog_name, 
            COUNT(s.id) as total
        FROM 
            studentorg_program prog
        LEFT JOIN 
            studentorg_student s ON s.program_id = prog.id
        GROUP BY 
            prog.prog_name
        ORDER BY 
            total DESC
        LIMIT 5;
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()

    # Prepare data for bubble chart
    data = []
    colors = [
        "#1d7af3", "#f3545d", "#fdaf4b", "#59d05d", "#716aca"
    ]
    for idx, row in enumerate(rows):
        program, total = row
        # Bubble chart expects {x, y, r}
        data.append({
            "label": program,
            "backgroundColor": colors[idx % len(colors)],
            "data": [{
                "x": idx + 1,      # Just to spread bubbles horizontally
                "y": total,        # Student count
                "r": 10 + total    # Bubble size (adjust as needed)
            }]
        })

    return JsonResponse({"datasets": data})

class OrganizationList(ListView):
    model = Organization
    context_object_name = 'organization'
    template_name = 'org_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrganizationList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return qs

class OrganizationCreateView(CreateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_add.html'
    success_url = reverse_lazy('organization-list')

class OrganizationUpdateView(UpdateView):
    model = Organization
    form_class = OrganizationForm
    template_name = 'org_edit.html'
    success_url = reverse_lazy('organization-list')

class OrganizationDeleteView(DeleteView):
    model = Organization
    template_name = 'org_del.html'
    success_url = reverse_lazy('organization-list')

class OrgMemberList(ListView):
    model = OrgMember
    context_object_name = 'orgmember'
    template_name = 'orgmember_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(OrgMemberList, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(student__firstname__icontains=query) | Q(student__lastname__icontains=query) |  Q(organization__name__icontains=query))
        return qs

class OrgMemberCreateView(CreateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_add.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberUpdateView(UpdateView):
    model = OrgMember
    form_class = OrgMemberForm
    template_name = 'orgmember_edit.html'
    success_url = reverse_lazy('orgmember-list')

class OrgMemberDeleteView(DeleteView):
    model = OrgMember
    template_name = 'orgmember_del.html'
    success_url = reverse_lazy('orgmember-list')

class StudentListView(ListView):
    model = Student
    context_object_name = 'student_list'
    template_name = 'student_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(StudentListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(firstname__icontains=query) | Q(lastname__icontains=query)
            )
        return qs

class StudentCreateView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_add.html'
    success_url = reverse_lazy('student-list')

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student_edit.html'
    success_url = reverse_lazy('student-list')

class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'student_del.html'
    success_url = reverse_lazy('student-list')

class CollegeListView(ListView):
    model = College
    context_object_name = 'college_list'
    template_name = 'college_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
            qs = super(CollegeListView, self).get_queryset(*args, **kwargs)
            if self.request.GET.get('q') is not None:
                query = self.request.GET.get('q')
                qs = qs.filter(Q(college_name__icontains=query))
            return qs

class CollegeCreateView(CreateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_add.html'
    success_url = reverse_lazy('college-list')

class CollegeUpdateView(UpdateView):
    model = College
    form_class = CollegeForm
    template_name = 'college_edit.html'
    success_url = reverse_lazy('college-list')

    def form_valid(self, form):
        college_name = form.instance.college_name
        messages.success(self.request, f'College "{college_name}" has been successfully updated.')

        return super().form_valid(form)

class CollegeDeleteView(DeleteView):
    model = College
    template_name = 'college_del.html'
    success_url = reverse_lazy('college-list')

class ProgramListView(ListView):
    model = Program
    context_object_name = 'program_list'
    template_name = 'program_list.html'
    paginate_by = 5

    def get_queryset(self, *args, **kwargs):
        qs = super(ProgramListView, self).get_queryset(*args, **kwargs)
        if self.request.GET.get('q') is not None:
            query = self.request.GET.get('q')
            qs = qs.filter(
                Q(prog_name__icontains=query) | Q(college__college_name__icontains=query)
            )
        return qs

class ProgramCreateView(CreateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_add.html'
    success_url = reverse_lazy('program-list')

class ProgramUpdateView(UpdateView):
    model = Program
    form_class = ProgramForm
    template_name = 'program_edit.html'
    success_url = reverse_lazy('program-list')

class ProgramDeleteView(DeleteView):
    model = Program
    template_name = 'program_del.html'
    success_url = reverse_lazy('program-list')

class BoatCreateView(CreateView):
    model = Boat
    fields = "__all__"
    template_name = "boat_form.html"
    success_url = reverse_lazy('boat-list')

    def post(self, request, *args, **kwargs):
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Validate dimensions
        errors = []
        for field_name, value in [('length', length), ('width', width), ('height', height)]:
            try:
                if float(value) <= 0:
                    errors.append(f"{field_name.capitalize()} must be greater than 0.")
            except (ValueError, TypeError):
                errors.append(f"{field_name.capitalize()} must be a valid number.")

        # If errors exist, display them and return to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())

        # Call the parent's post() if validation passes
        return super().post(request, *args, **kwargs)

class BoatUpdateView(UpdateView):
    model = Boat
    fields = "__all__"
    template_name = "boat_form.html"
    success_url = reverse_lazy('boat-list')

    def post(self, request, *args, **kwargs):
        length = request.POST.get('length')
        width = request.POST.get('width')
        height = request.POST.get('height')

        # Validate dimensions
        errors = []
        for field_name, value in [('length', length), ('width', width), ('height', height)]:
            try:
                if float(value) <= 0:
                    errors.append(f"{field_name.capitalize()} must be greater than 0.")
            except (ValueError, TypeError):
                errors.append(f"{field_name.capitalize()} must be a valid number.")

        # If errors exist, display them and return to the form
        if errors:
            for error in errors:
                messages.error(request, error)
            return self.form_invalid(self.get_form())

        # Call the parent's post() if validation passes
        return super().post(request, *args, **kwargs)

# Create your views here.