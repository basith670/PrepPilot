from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Topic(models.Model):

    DIFFICULTY_CHOICES = [

        ("Easy", "Easy"),

        ("Medium", "Medium"),

        ("Hard", "Hard"),

    ]

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("In Progress", "In Progress"),

        ("Completed", "Completed"),

    ]

    subject = models.ForeignKey(

        Subject,

        on_delete=models.CASCADE,

        related_name="topics"

    )

    title = models.CharField(

        max_length=150

    )

    description = models.TextField()

    difficulty = models.CharField(

        max_length=20,

        choices=DIFFICULTY_CHOICES,

        default="Medium"

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Pending"

    )

    estimated_hours = models.PositiveIntegerField(

        default=1

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    updated_at = models.DateTimeField(

        auto_now=True

    )

    def __str__(self):

        return self.title
    

class Resume(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    null=True,
    blank=True
)

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    resume = models.FileField(
        upload_to="resumes/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name
    

class Company(models.Model):

    STATUS_CHOICES = [

        ("Applied", "Applied"),

        ("OA", "Online Assessment"),

        ("Technical", "Technical Interview"),

        ("HR", "HR Interview"),

        ("Selected", "Selected"),

        ("Rejected", "Rejected"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(
        max_length=100
    )

    role = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100
    )

    package = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    application_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Applied"
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.company_name
    
class Profile(models.Model):

    user = models.OneToOneField(

        User,

        on_delete=models.CASCADE

    )

    profile_image = models.ImageField(

        upload_to="profiles/",

        blank=True,

        null=True

    )

    full_name = models.CharField(

        max_length=100,

        blank=True

    )

    phone = models.CharField(

        max_length=15,

        blank=True

    )

    college = models.CharField(

        max_length=150,

        blank=True

    )

    degree = models.CharField(

        max_length=100,

        blank=True

    )

    branch = models.CharField(

        max_length=100,

        blank=True

    )

    graduation_year = models.PositiveIntegerField(

        blank=True,

        null=True

    )

    linkedin = models.URLField(

        blank=True

    )

    github = models.URLField(

        blank=True

    )

    bio = models.TextField(

        blank=True

    )

    def __str__(self):

        return self.user.username
    
class Event(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    event_date = models.DateField()

    event_time = models.TimeField()

    EVENT_TYPES = [

        ("Study", "Study"),

        ("Interview", "Interview"),

        ("Deadline", "Deadline"),

        ("Exam", "Exam"),

        ("Meeting", "Meeting"),

    ]

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        default="Study"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title
    
class StudyPlan(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    target_company = models.CharField(
        max_length=100
    )

    study_hours = models.PositiveIntegerField()

    exam_date = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.user.username} - {self.target_company}"
    

class InterviewSession(models.Model):

    COMPANY_CHOICES = [

        ("Google", "Google"),
        ("Microsoft", "Microsoft"),
        ("Amazon", "Amazon"),
        ("Infosys", "Infosys"),
        ("TCS", "TCS"),
        ("Accenture", "Accenture"),
        ("Wipro", "Wipro"),
        ("Cognizant", "Cognizant"),
        ("Capgemini", "Capgemini"),

    ]

    ROLE_CHOICES = [

        ("Python Developer", "Python Developer"),
        ("Full Stack Developer", "Full Stack Developer"),
        ("Frontend Developer", "Frontend Developer"),
        ("Backend Developer", "Backend Developer"),
        ("Java Developer", "Java Developer"),
        ("Data Analyst", "Data Analyst"),

    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    company = models.CharField(
        max_length=100,
        choices=COMPANY_CHOICES
    )

    role = models.CharField(
        max_length=100,
        choices=ROLE_CHOICES
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.company} - {self.role}"
    
class InterviewQuestion(models.Model):

    CATEGORY_CHOICES = [

        ("Technical", "Technical"),

        ("Coding", "Coding"),

        ("HR", "HR"),

        ("Aptitude", "Aptitude"),

    ]

    DIFFICULTY_CHOICES = [

        ("Easy", "Easy"),

        ("Medium", "Medium"),

        ("Hard", "Hard"),

    ]

    session = models.ForeignKey(

        InterviewSession,

        on_delete=models.CASCADE,

        related_name="questions"

    )

    question = models.TextField()

    category = models.CharField(

        max_length=20,

        choices=CATEGORY_CHOICES,

        default="Technical"

    )

    difficulty = models.CharField(

        max_length=20,

        choices=DIFFICULTY_CHOICES,

        default="Medium"

    )

    practiced = models.BooleanField(

        default=False

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return self.question[:60]
    
class UserSettings(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    email_notifications = models.BooleanField(
        default=True
    )

    study_reminders = models.BooleanField(
        default=True
    )

    interview_reminders = models.BooleanField(
        default=True
    )

    placement_alerts = models.BooleanField(
        default=True
    )

    dark_mode = models.BooleanField(
        default=False
    )

    def __str__(self):

        return self.user.username