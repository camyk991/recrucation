from django import forms
from .models import User, StudentsData, StudentCandidate, SelectedFieldOfStudy, StudentDocuments, FieldOfStudy
from django.contrib.auth.forms import UserCreationForm


class CandidateRegistrationForm(UserCreationForm):
    # Pola do danych osobowych
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    pesel = forms.CharField(max_length=11, required=False)
    telephone_number = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'name', 'surname', 'email', 'pesel', 'telephone_number')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'candidate'
        if commit:
            user.save()
            # Zapisz dane osobowe
            students_data = StudentsData.objects.create(
                name=self.cleaned_data['name'],
                surname=self.cleaned_data['surname'],
                email=self.cleaned_data['email'],
                pesel=self.cleaned_data.get('pesel', ''),
                telephone_number=self.cleaned_data['telephone_number']
            )
            # Powiąż usera z danymi osobowymi
            user.students_data = students_data
            # Stwórz obiekt StudentCandidate
            candidate = StudentCandidate.objects.create()
            user.student_candidate = candidate
            user.save()
        return user

class StudentsDataForm(forms.ModelForm):
    class Meta:
        model = StudentsData
        fields = ['name', 'surname', 'email', 'pesel', 'telephone_number']

class StudentCandidateForm(forms.ModelForm):
    class Meta:
        model = StudentCandidate
        fields = ['date_of_document_transfer']


class SelectedFieldOfStudyForm(forms.ModelForm):
    field_of_study = forms.ModelChoiceField(queryset=FieldOfStudy.objects.all())

    class Meta:
        model = SelectedFieldOfStudy
        fields = ['field_of_study', 'priority_number', 'recruitment_points', 'status', 'is_candidate_paid']
        widgets = {
            'status': forms.HiddenInput(),  # status ustawimy np. domyślnie na 'kandydat'
            'is_candidate_paid': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = 'kandydat'
        self.fields['is_candidate_paid'].initial = False


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = StudentDocuments
        fields = ['document']
