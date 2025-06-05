from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('candidate', 'Candidate'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    student_candidate = models.OneToOneField('StudentCandidate', on_delete=models.SET_NULL, null=True, blank=True)
    students_data = models.OneToOneField('StudentsData', on_delete=models.CASCADE, null=True, blank=True)

class StudentsData(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=50)
    pesel = models.CharField(max_length=11, blank=True, null=True)
    telephone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} {self.surname}"

class StudentCandidate(models.Model):
    date_of_document_transfer = models.DateField(null=True, blank=True)
    archive_requested = models.BooleanField(default=False)

    def __str__(self):
        return f"Kandydat {self.id}"

class StudentDocuments(models.Model):
    student_candidate = models.ForeignKey(StudentCandidate, on_delete=models.CASCADE)
    document = models.FileField(upload_to='documents/')  # zamiast BinaryField


class FieldOfStudy(models.Model):
    DEGREE_CHOICES = (
        ('inz', 'Inżynierskie'),
        ('mgr', 'Magisterskie'),
        ('dr', 'Doktoranckie'),
    )
    name = models.CharField(max_length=30)
    degree_of_studies = models.CharField(max_length=3, choices=DEGREE_CHOICES)
    min_recruitment_points = models.FloatField()
    max_number_of_students = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.degree_of_studies})"

class SelectedFieldOfStudy(models.Model):
    STATUS_CHOICES = (
        ('kandydat', 'Kandydat'),
        ('oczekujacy', 'Oczekujący'),
        ('odrzucony', 'Odrzucony'),
        ('zakwalifikowany', 'Zakwalifikowany'),
        ('niezakwalifikowany', 'Niezakwalifikowany'),
    )
    student_candidate = models.ForeignKey(StudentCandidate, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldOfStudy, on_delete=models.CASCADE)
    priority_number = models.IntegerField()
    recruitment_points = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    is_candidate_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student_candidate', 'field_of_study', 'priority_number')

    def __str__(self):
        return f"{self.student_candidate} - {self.field_of_study} (priorytet: {self.priority_number})"
