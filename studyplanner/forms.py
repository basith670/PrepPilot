from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InterviewSession, InterviewQuestion

from .models import (
    Resume,
    Subject,
    Topic,
    Company,
    Profile,
    Event,
    StudyPlan,
    InterviewSession,
    InterviewQuestion,
    UserSettings,
)


class ResumeForm(forms.ModelForm):

    class Meta:

        model = Resume

        fields = [

            "name",

            "email",

            "resume",

        ]

        widgets = {

            "name": forms.TextInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Full Name"

                }

            ),

            "email": forms.EmailInput(

                attrs={

                    "class": "form-control",

                    "placeholder": "Enter Email Address"

                }

            ),

            "resume": forms.ClearableFileInput(

                attrs={

                    "class": "form-control"

                }

            ),

        }


class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]


class SubjectForm(forms.ModelForm):

    class Meta:

        model = Subject

        fields = [
            "name",
            "description"
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Subject"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Description"
                }
            )

        }


class TopicForm(forms.ModelForm):

    class Meta:

        model = Topic

        fields = [
            "subject",
            "title",
            "description",
            "difficulty",
            "status",
            "estimated_hours"
        ]

        widgets = {

            "subject": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Topic Name"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter Description"
                }
            ),

            "difficulty": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "estimated_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            )

        }
class CompanyForm(forms.ModelForm):

    class Meta:

        model = Company

        fields = [

            "company_name",

            "role",

            "location",

            "package",

            "application_date",

            "status",

        ]

        widgets = {

            "company_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Company Name"
                }
            ),

            "role": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Job Role"
                }
            ),

            "location": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Location"
                }
            ),

            "package": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "step": "0.01",
                    "placeholder": "Package (LPA)"
                }
            ),

            "application_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }

class ProfileForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = [

            "profile_image",

            "full_name",

            "phone",

            "college",

            "degree",

            "branch",

            "graduation_year",

            "linkedin",

            "github",

            "bio",

        ]

        widgets = {

            "profile_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control"
                }
            ),

            "full_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Full Name"
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number"
                }
            ),

            "college": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter College Name"
                }
            ),

            "degree": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: B.Tech"
                }
            ),

            "branch": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Computer Science"
                }
            ),

            "graduation_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2027"
                }
            ),

            "linkedin": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://linkedin.com/in/username"
                }
            ),

            "github": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://github.com/username"
                }
            ),

            "bio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write something about yourself..."
                }
            ),
        }

class EventForm(forms.ModelForm):

    class Meta:

        model = Event

        fields = [

            "title",

            "description",

            "event_type",

            "event_date",

            "event_time",

        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Event Title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4
                }
            ),

            "event_type": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "event_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

            "event_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time"
                }
            ),

        }

class StudyPlanForm(forms.ModelForm):

    class Meta:

        model = StudyPlan

        fields = [

            "target_company",

            "study_hours",

            "exam_date",

        ]

        widgets = {

            "target_company": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Google / TCS / Infosys"
                }
            ),

            "study_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 1
                }
            ),

            "exam_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date"
                }
            ),

        }

class InterviewSessionForm(forms.ModelForm):

    class Meta:

        model = InterviewSession

        fields = [

            "company",

            "role",

        ]

        widgets = {

            "company": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "role": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

        }

class UserSettingsForm(forms.ModelForm):

    class Meta:

        model = UserSettings

        fields = [

            "email_notifications",

            "study_reminders",

            "interview_reminders",

            "placement_alerts",

            "dark_mode",

        ]

        widgets = {

            "email_notifications": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "study_reminders": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "interview_reminders": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "placement_alerts": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

            "dark_mode": forms.CheckboxInput(

                attrs={
                    "class": "form-check-input"
                }

            ),

        }