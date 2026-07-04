from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [

    # Dashboard
    path("", views.dashboard, name="dashboard"),
    path("dashboard/", views.dashboard, name="dashboard"),

    # AI Study Planner
    path(
        "ai-study-planner/",
        views.ai_study_planner,
        name="ai_study_planner",
    ),

    # Subjects
    path(
        "subjects/",
        views.subjects,
        name="subjects",
    ),

    path(
        "subjects/add/",
        views.add_subject,
        name="add_subject",
    ),

    path(
        "subjects/edit/<int:id>/",
        views.edit_subject,
        name="edit_subject",
    ),

    path(
        "subjects/delete/<int:id>/",
        views.delete_subject,
        name="delete_subject",
    ),

    path(
        "subjects/<int:id>/",
        views.subject_detail,
        name="subject_detail",
    ),

    # Topics
    path(
        "topics/",
        views.topics,
        name="topics",
    ),

    path(
        "topics/add/",
        views.add_topic,
        name="add_topic",
    ),

    path(
        "topics/edit/<int:id>/",
        views.edit_topic,
        name="edit_topic",
    ),

    path(
        "topics/delete/<int:id>/",
        views.delete_topic,
        name="delete_topic",
    ),

    # Placement Tracker
    path(
        "placement/",
        views.placement,
        name="placement",
    ),

    path(
        "placement/add/",
        views.add_company,
        name="add_company",
    ),

    path(
        "placement/edit/<int:id>/",
        views.edit_company,
        name="edit_company",
    ),

    path(
        "placement/delete/<int:id>/",
        views.delete_company,
        name="delete_company",
    ),

    # Placement Readiness
    path(
        "placement-readiness/",
        views.placement_readiness,
        name="placement_readiness",
    ),

    # Mock Interview (current interview page)
    path(
        "interview/",
        views.interview,
        name="interview",
    ),

    # Resume
    path(
        "resume/",
        views.resume,
        name="resume",
    ),

    path(
        "resume/edit/<int:id>/",
        views.edit_resume,
        name="edit_resume",
    ),

    path(
        "resume/delete/<int:id>/",
        views.delete_resume,
        name="delete_resume",
    ),

    # Profile
    path(
        "profile/",
        views.profile,
        name="profile",
    ),

    path(
        "profile/edit/",
        views.edit_profile,
        name="edit_profile",
    ),

    # Calendar
    path(
        "calendar/",
        views.calendar,
        name="calendar",
    ),

    path(
        "calendar/add/",
        views.add_event,
        name="add_event",
    ),

    path(
        "calendar/edit/<int:id>/",
        views.edit_event,
        name="edit_event",
    ),

    path(
        "calendar/delete/<int:id>/",
        views.delete_event,
        name="delete_event",
    ),

    # Analytics
    path(
        "analytics/",
        views.analytics,
        name="analytics",
    ),

    # Settings
    path(
        "settings/",
        views.settings,
        name="settings",
    ),

    # Authentication
    path(
        "register/",
        views.register,
        name="register",
    ),

    path(
        "login/",
        views.login_view,
        name="login",
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),

    path(
    "interview/practiced/<int:id>/",
    views.mark_practiced,
    name="mark_practiced",
),

path(
    "password-change/",
    auth_views.PasswordChangeView.as_view(
        template_name="password_change.html"
    ),
    name="password_change",
),

path(
    "password-change/done/",
    auth_views.PasswordChangeDoneView.as_view(
        template_name="password_change_done.html"
    ),
    name="password_change_done",
),
]