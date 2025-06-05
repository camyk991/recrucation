from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .models import StudentsData, StudentCandidate, SelectedFieldOfStudy, StudentDocuments, FieldOfStudy
from .forms import StudentsDataForm, StudentCandidateForm, SelectedFieldOfStudyForm, CandidateRegistrationForm, DocumentUploadForm, SelectedFieldOfStudyForm

@login_required
def candidates_list(request):
    candidates = SelectedFieldOfStudy.objects.filter(is_candidate_paid=True).select_related('student_candidate', 'field_of_study')
    context = {'candidates': candidates}
    return render(request, 'candidates_list.html', context)

@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(StudentCandidate, pk=pk)
    student_data = candidate.studentsdata_set.first()
    selected_fields = SelectedFieldOfStudy.objects.filter(student_candidate=candidate)
    context = {'candidate': candidate, 'student_data': student_data, 'selected_fields': selected_fields}
    return render(request, 'candidate_detail.html', context)

@login_required
def add_candidate(request):
    if request.method == 'POST':
        students_form = StudentsDataForm(request.POST)
        candidate_form = StudentCandidateForm(request.POST)
        if students_form.is_valid() and candidate_form.is_valid():
            student_data = students_form.save()
            candidate = candidate_form.save(commit=False)
            candidate.studentsdata = student_data
            candidate.save()
            return redirect('candidates_list')
    else:
        students_form = StudentsDataForm()
        candidate_form = StudentCandidateForm()
    return render(request, 'add_candidate.html', {'students_form': students_form, 'candidate_form': candidate_form})

def register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # automatyczne logowanie po rejestracji
            return redirect('candidates_list')
    else:
        form = CandidateRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    user = request.user
    # Dane osobowe (można edytować)
    students_data = user.students_data
    if request.method == 'POST':
        students_form = StudentsDataForm(request.POST, instance=students_data)
        doc_form = DocumentUploadForm(request.POST or None, request.FILES or None)
        field_form = SelectedFieldOfStudyForm(request.POST)

        if 'save_personal' in request.POST and students_form.is_valid():
            students_form.save()
            return redirect('dashboard')

        elif 'upload_doc' in request.POST and doc_form.is_valid():
            doc = doc_form.save(commit=False)
            doc.student_candidate = user.student_candidate
            doc.save()
            return redirect('dashboard')

        elif 'declare_field' in request.POST and field_form.is_valid():
            field = field_form.save(commit=False)
            field.student_candidate = user.student_candidate
            field.save()
            return redirect('dashboard')

    else:
        students_form = StudentsDataForm(instance=students_data)
        doc_form = DocumentUploadForm()
        field_form = SelectedFieldOfStudyForm()

    # Lista dostępnych kierunków do wyboru (formularz field_form to zapewnia)
    declared_fields = SelectedFieldOfStudy.objects.filter(student_candidate=user.student_candidate)

    context = {
        'students_form': students_form,
        'doc_form': doc_form,
        'field_form': field_form,
        'declared_fields': declared_fields,
        'is_admin': user.role == 'admin',
    }
    return render(request, 'dashboard.html', context)