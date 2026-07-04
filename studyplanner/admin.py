from django.contrib import admin

from .models import (
    Subject,
    Topic,
    Resume,
    Company,
    Profile,
    Event,
    StudyPlan,
    InterviewSession,
    InterviewQuestion,
    UserSettings,
)

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(StudyPlan)
admin.site.register(InterviewSession)
admin.site.register(InterviewQuestion)
admin.site.register(UserSettings)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "description",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "subject",
    )

    search_fields = (
        "title",
    )

    list_filter = (
        "subject",
    )

    ordering = (
        "title",
    )


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "uploaded_at",
    )

    search_fields = (
        "name",
        "email",
    )

    ordering = (
        "-uploaded_at",
    )

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = (
        "company_name",
        "role",
        "status",
        "package",
        "application_date",
    )

    search_fields = (
        "company_name",
        "role",
    )

    list_filter = (
        "status",
        "location",
    )

    ordering = (
        "-application_date",
    )
    