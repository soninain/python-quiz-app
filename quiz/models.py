from django.db import models


# Create your models here.
class UserInfo(models.Model):
    email = models.EmailField(max_length=254, unique=True, null=True, blank=True)
    password = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        db_table = "user_info"


class Course(models.Model):
    # FIX: removed `objects = None` which was overriding the default manager and breaking Course.objects.all() etc.
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to="images/")
    course_des = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.course_name

    class Meta:
        db_table = "Course"


class Questions(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    question = models.CharField(max_length=500, null=True)
    answer = models.CharField(max_length=100, default=None, blank=True, null=True)
    option_one = models.CharField(max_length=100, blank=True, null=True)
    option_two = models.CharField(max_length=100, blank=True, null=True)
    markes = models.IntegerField(default=5, blank=True, null=True)

    def __str__(self):
        return self.question

    class Meta:
        db_table = "quiz"


class ContactForm(models.Model):
    name = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(
        max_length=254, null=True, blank=True
    )  # FIX: removed unique=True — allows multiple contact submissions
    message = models.TextField(null=True, blank=True)


class QuizResult(models.Model):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)

    total_marks = models.IntegerField(default=0)
    obtained_marks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.course.course_name}"

    class Meta:
        db_table = "quiz_result"
