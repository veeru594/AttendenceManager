from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

DAYS_CHOICES = [
    ('mon', 'Monday'), 
    ('tue', 'Tuesday'), 
    ('wed', 'Wednesday'), 
    ('thu', 'Thursday'), 
    ('fri', 'Friday'), 
    ('sat', 'Saturday')
]

LEAVE_CHOICES = [
    ('ml', 'Medical Leave'), 
    ('od', 'On Duty')
]

class Slot(models.Model):
    period_id = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Department(models.Model):
    dept_id = models.CharField(max_length=20, primary_key=True)
    dept_name = models.CharField(max_length=50)
    
class Admin(models.Model):
    admin_id = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=30)

class Class(models.Model):
    class_id = models.CharField(max_length=20, primary_key=True)
    total_students = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

class Student(models.Model):
    stud_id = models.CharField(max_length=20, primary_key=True)
    s_password = models.CharField(max_length=30)
    in_out = models.CharField(max_length=5)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)

class Faculty(models.Model):
    fac_id = models.CharField(max_length=20, primary_key=True)
    f_password = models.CharField(max_length=30)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    dept_id = models.ForeignKey(Department, on_delete=models.CASCADE)

class Calender(models.Model):
    date = models.DateField(primary_key=True)
    day = models.CharField(max_length=9, choices=DAYS_CHOICES, default=None, blank=False)

class Course(models.Model):
    course_id = models.CharField(max_length=20, primary_key=True)
    course_name = models.CharField(max_length=50)
    credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class Attendance(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    presence = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1)])
    periods = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=9)  # Assuming 1 is the default period value

    class Meta:
        unique_together = (("stud_id", "course_id", "date"),)


class Holiday(models.Model):
    date = models.DateField(primary_key=True)
    description = models.CharField(max_length=100)

class Leave(models.Model):
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    leave_type = models.CharField(max_length=9, choices=LEAVE_CHOICES, default=None, blank=False)
    approved = models.BooleanField(default=False)

class Timetable(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=9, choices=DAYS_CHOICES, default=None, blank=False)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    period_id = models.ForeignKey(Slot, on_delete=models.CASCADE, null=True)
    class Meta:
        unique_together = (("class_id", "course_id", "day", "period_id"),)

class Teache(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    class Meta:
        unique_together = (("course_id", "class_id"),)
