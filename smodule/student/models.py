from django.db import models

# Create your models here.
from django.db import models

# Table 1: Student Table
class Student(models.Model):
    roll_number = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    cgpa = models.FloatField()

    def __str__(self):
        return self.name

# Table 2: Company Table 
# class Company(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.company_name

class Company(models.Model):
    rollno = models.ForeignKey(Student, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255,default='unknown')
    company_role = models.CharField(max_length=255,default='unknown')
    years_of_experience = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.rollno.roll_number}'


# Table 4: Guide Table 
class Guide(models.Model):
    guide_name = models.CharField(max_length=100)
    guide_code = models.CharField(max_length=5)

    def __str__(self):
        return self.guide_name



# class Preference(models.Model):
#     student = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)
#     preference1 = models.CharField(max_length=100, blank=True, null=True)
#     preference2 = models.CharField(max_length=100, blank=True, null=True)
#     preference3 = models.CharField(max_length=100, blank=True, null=True)
#     preference4 = models.CharField(max_length=100, blank=True, null=True)
#     preference5 = models.CharField(max_length=100, blank=True, null=True)
#     preference6 = models.CharField(max_length=100, blank=True, null=True)
#     preference7 = models.CharField(max_length=100, blank=True, null=True)
#     preference8 = models.CharField(max_length=100, blank=True, null=True)
#     preference9 = models.CharField(max_length=100, blank=True, null=True)
#     preference10 = models.CharField(max_length=100, blank=True, null=True)

#     def __str__(self):
#         return f"Preferences for {self.student.name}"

class UserPreference(models.Model):
    rollno = models.OneToOneField(Student, on_delete=models.CASCADE, primary_key=True)  # Roll number field
    preferences = models.JSONField(default=list)  # Store preferences as a JSON list
    is_final = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.rollno.roll_number}'

    
from django.utils import timezone

class PreferenceTimeframe(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    allotment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Preference timeframe from {self.start_time} to {self.end_time} with allotment at {self.allotment_time}"
      

class Faculty(models.Model):
    teacher_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, default='studentmail.sid0+DN@gmail.com')
    willingness = models.BooleanField(default=False)

    def __str__(self):
        return self.name
