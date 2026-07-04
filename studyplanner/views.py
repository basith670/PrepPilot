from django.shortcuts import (
    render,
    redirect,
    get_object_or_404,
)

from django.contrib.auth import (
    login,
    logout,
    authenticate,
)

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.core.paginator import Paginator

from django.db.models import Count

from datetime import date, timedelta
from django.utils import timezone

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

from .forms import (
    ResumeForm,
    RegisterForm,
    SubjectForm,
    TopicForm,
    CompanyForm,
    ProfileForm,
    EventForm,
    StudyPlanForm,
    InterviewSessionForm,
    UserSettingsForm,
)

@login_required
def dashboard(request):

    # ==========================
    # DYNAMIC GREETING
    # ==========================

    current_hour = timezone.localtime().hour

    if 5 <= current_hour < 12:
        greeting = "🌅 Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "☀️ Good Afternoon"
    elif 17 <= current_hour < 21:
        greeting = "🌇 Good Evening"
    else:
        greeting = "🌙 Good Night"

    # ==========================
    # SUBJECTS & TOPICS
    # ==========================

    subject_count = Subject.objects.filter(
        user=request.user
    ).count()

    topic_queryset = Topic.objects.filter(
        subject__user=request.user
    )

    topic_count = topic_queryset.count()

    completed_count = topic_queryset.filter(
        status="Completed"
    ).count()

    pending_count = topic_queryset.filter(
        status="Pending"
    ).count()

    progress_count = topic_queryset.filter(
        status="In Progress"
    ).count()

    total_hours = sum(
        topic.estimated_hours
        for topic in topic_queryset
    )

    if topic_count > 0:

        completion_percentage = round(
            (completed_count / topic_count) * 100
        )

    else:

        completion_percentage = 0

    # ==========================
    # STUDY STREAK
    # ==========================

    completed_today = topic_queryset.filter(
        status="Completed"
    ).exists()

    if completed_today:

        study_streak = 1

        streak_message = (
            "Great job! Keep the momentum going."
        )

    else:

        study_streak = 0

        streak_message = (
            "Complete a topic today to start your streak."
        )

    # ==========================
    # RESUMES
    # ==========================

    resume_count = Resume.objects.filter(
        user=request.user
    ).count()

    # ==========================
    # PLACEMENT
    # ==========================

    company_queryset = Company.objects.filter(
        user=request.user
    )

    application_count = company_queryset.count()

    selected_count = company_queryset.filter(
        status="Selected"
    ).count()

    interview_count = company_queryset.filter(
        status__in=[
            "Technical",
            "HR"
        ]
    ).count()

    # ==========================
    # UPCOMING EVENTS
    # ==========================

    upcoming_events = Event.objects.filter(
        user=request.user,
        event_date__gte=date.today()
    ).order_by(
        "event_date"
    )[:5]

    # ==========================
    # RECENT TOPICS
    # ==========================

    recent_topics = Topic.objects.filter(
        subject__user=request.user
    ).order_by(
        "-updated_at"
    )[:5]

    # ==========================
    # RECENT COMPANIES
    # ==========================

    recent_companies = Company.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )[:5]

    # ==========================
    # PLACEMENT READINESS
    # ==========================

    placement_readiness = round(

        (completion_percentage * 0.40)

        +

        (min(application_count, 10) * 3)

        +

        (min(resume_count, 1) * 30)

    )

    if placement_readiness > 100:

        placement_readiness = 100

    # ==========================
    # NOTIFICATIONS
    # ==========================

    today = date.today()

    upcoming_notifications = Event.objects.filter(
        user=request.user,
        event_date__gte=today
    ).order_by(
        "event_date"
    )[:5]

    pending_notifications = Topic.objects.filter(
        subject__user=request.user,
        status="Pending"
    ).count()

    interview_notifications = Company.objects.filter(
        user=request.user,
        status__in=[
            "Technical",
            "HR"
        ]
    ).count()

    # ==========================
    # CONTEXT
    # ==========================

    context = {

        # Greeting

        "greeting": greeting,

        # Dashboard Cards

        "subject_count": subject_count,

        "topic_count": topic_count,

        "resume_count": resume_count,

        "application_count": application_count,

        # Topic Statistics

        "completed_count": completed_count,

        "pending_count": pending_count,

        "progress_count": progress_count,

        "completion_percentage": completion_percentage,

        "total_hours": total_hours,

        # Study Streak

        "study_streak": study_streak,

        "streak_message": streak_message,

        # Placement

        "selected_count": selected_count,

        "interview_count": interview_count,

        "placement_readiness": placement_readiness,

        # Dashboard Sections

        "upcoming_events": upcoming_events,

        "recent_topics": recent_topics,

        "recent_companies": recent_companies,

        # Notifications

        "upcoming_notifications": upcoming_notifications,

        "pending_notifications": pending_notifications,

        "interview_notifications": interview_notifications,

    }

    return render(
        request,
        "dashboard.html",
        context
    )

@login_required
def studyplanner(request):

    return render(
        request,
        "studyplanner.html"
    )

@login_required
def subjects(request):

    # Search & Sort
    search = request.GET.get("search", "")
    sort = request.GET.get("sort", "newest")

    # Logged-in user's subjects
    subjects = Subject.objects.filter(
        user=request.user
    )

    # Search
    if search:
        subjects = subjects.filter(
            name__icontains=search
        )

    # Sorting
    if sort == "newest":
        subjects = subjects.order_by("-created_at")

    elif sort == "oldest":
        subjects = subjects.order_by("created_at")

    elif sort == "az":
        subjects = subjects.order_by("name")

    elif sort == "za":
        subjects = subjects.order_by("-name")

    # Pagination
    paginator = Paginator(subjects, 6)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    # Subject Cards
    subject_data = []

    for subject in page_obj:

        topics = Topic.objects.filter(
            subject=subject
        )

        total_topics = topics.count()

        completed_topics = topics.filter(
            status="Completed"
        ).count()

        pending_topics = topics.exclude(
            status="Completed"
        ).count()

        if total_topics > 0:

            progress = int(
                (completed_topics / total_topics) * 100
            )

        else:

            progress = 0

        subject_data.append({

    "subject": subject,

    "total_topics": total_topics,

    "completed_topics": completed_topics,

    "pending_topics": pending_topics,

    "progress": progress,

    "progress_color": (
        "bg-danger"
        if progress <= 30
        else "bg-warning"
        if progress <= 60
        else "bg-success"
    ),

})

    # Overall Statistics
    all_subjects = Subject.objects.filter(
        user=request.user
    )

    all_topics = Topic.objects.filter(
        subject__user=request.user
    )

    total_subjects = all_subjects.count()

    total_topics = all_topics.count()

    completed_topics = all_topics.filter(
        status="Completed"
    ).count()

    pending_topics = all_topics.exclude(
        status="Completed"
    ).count()

    if total_topics > 0:

        overall_progress = int(
            (completed_topics / total_topics) * 100
        )

    else:

        overall_progress = 0

    context = {

        "subject_data": subject_data,

        "page_obj": page_obj,

        "search": search,

        "sort": sort,

        "subject_count": paginator.count,

        "total_subjects": total_subjects,

        "total_topics": total_topics,

        "completed_topics": completed_topics,

        "pending_topics": pending_topics,

        "overall_progress": overall_progress,

    }

    return render(
        request,
        "subjects.html",
        context
    )


@login_required
def add_subject(request):

    if request.method == "POST":

        form = SubjectForm(request.POST)

        if form.is_valid():

            subject = form.save(commit=False)

            subject.user = request.user

            subject.save()

            messages.success(
        request,
        "Subject added successfully."
)

            return redirect("subjects")

    else:

        form = SubjectForm()

    return render(
        request,
        "add_subject.html",
        {
            "form": form
        }
    )

@login_required
def subject_detail(request, id):

    subject = get_object_or_404(
        Subject,
        id=id,
        user=request.user
    )

    topics = Topic.objects.filter(
        subject=subject
    ).order_by("title")

    total_topics = topics.count()

    completed_topics = topics.filter(
        status="Completed"
    ).count()

    pending_topics = topics.filter(
        status="Pending"
    ).count()

    inprogress_topics = topics.filter(
        status="In Progress"
    ).count()

    estimated_hours = sum(
        topic.estimated_hours
        for topic in topics
    )

    progress = 0

    if total_topics > 0:

        progress = int(
            (completed_topics / total_topics) * 100
        )

    context = {

        "subject": subject,

        "topics": topics,

        "total_topics": total_topics,

        "completed_topics": completed_topics,

        "pending_topics": pending_topics,

        "inprogress_topics": inprogress_topics,

        "estimated_hours": estimated_hours,

        "progress": progress,

    }

    return render(
        request,
        "subject_detail.html",
        context
    )

@login_required
def topics(request):

    search = request.GET.get("search", "")

    subject = request.GET.get("subject", "")

    status = request.GET.get("status", "")

    sort = request.GET.get("sort", "newest")

    topics = Topic.objects.filter(
        subject__user=request.user
    )

    # Search

    if search:

        topics = topics.filter(
            title__icontains=search
        )

    # Subject Filter

    if subject:

        topics = topics.filter(
            subject_id=subject
        )

    # Status Filter

    if status:

        topics = topics.filter(
            status=status
        )

    # Sorting

    if sort == "newest":

        topics = topics.order_by("-created_at")

    elif sort == "oldest":

        topics = topics.order_by("created_at")

    elif sort == "az":

        topics = topics.order_by("title")

    elif sort == "za":

        topics = topics.order_by("-title")

    # Pagination

    paginator = Paginator(
        topics,
        6
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    # Statistics

    all_topics = Topic.objects.filter(
        subject__user=request.user
    )

    total_topics = all_topics.count()

    completed_topics = all_topics.filter(
        status="Completed"
    ).count()

    pending_topics = all_topics.filter(
        status="Pending"
    ).count()

    inprogress_topics = all_topics.filter(
        status="In Progress"
    ).count()

    subjects = Subject.objects.filter(
        user=request.user
    )

    context = {

        "page_obj": page_obj,

        "topics": page_obj,

        "subjects": subjects,

        "search": search,

        "selected_subject": subject,

        "selected_status": status,

        "sort": sort,

        "total_topics": total_topics,

        "completed_topics": completed_topics,

        "pending_topics": pending_topics,

        "inprogress_topics": inprogress_topics,

    }

    return render(

        request,

        "topics.html",

        context

    )

@login_required
def add_topic(request):

    if request.method == "POST":

        form = TopicForm(request.POST)

        # Show only the logged-in user's subjects
        form.fields["subject"].queryset = Subject.objects.filter(
            user=request.user
        )

        if form.is_valid():

            form.save()

            return redirect("topics")

    else:

        form = TopicForm()

        form.fields["subject"].queryset = Subject.objects.filter(
            user=request.user
        )

    return render(
        request,
        "add_topic.html",
        {
            "form": form
        }
    )

@login_required
def edit_topic(request, id):

    topic = get_object_or_404(
        Topic,
        id=id
    )

    if request.method == "POST":

        form = TopicForm(
            request.POST,
            instance=topic
        )

        if form.is_valid():

            form.save()

            return redirect("topics")

    else:

        form = TopicForm(instance=topic)

    return render(
        request,
        "edit_topic.html",
        {
            "form": form
        }
    )


@login_required
def delete_topic(request, id):

    topic = get_object_or_404(
        Topic,
        id=id
    )

    if request.method == "POST":

        topic.delete()

        return redirect("topics")

    return render(
        request,
        "delete_topic.html",
        {
            "topic": topic
        }
    )

@login_required
def placement(request):

    companies = Company.objects.filter(
        user=request.user
    )

    search = request.GET.get("search", "")

    status = request.GET.get("status", "")

    sort = request.GET.get("sort", "newest")

    # Search

    if search:

        companies = companies.filter(
            company_name__icontains=search
        )

    # Status Filter

    if status:

        companies = companies.filter(
            status=status
        )

    # Sorting

    if sort == "package":

        companies = companies.order_by("-package")

    elif sort == "oldest":

        companies = companies.order_by("application_date")

    else:

        companies = companies.order_by("-application_date")

    # Statistics

    all_companies = Company.objects.filter(
        user=request.user
    )

    total_applications = all_companies.count()

    selected_count = all_companies.filter(
        status="Selected"
    ).count()

    rejected_count = all_companies.filter(
        status="Rejected"
    ).count()

    process_count = all_companies.exclude(
        status__in=["Selected", "Rejected"]
    ).count()

    # Pagination

    paginator = Paginator(
        companies,
        8
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        "companies": page_obj,

        "page_obj": page_obj,

        "search": search,

        "status": status,

        "sort": sort,

        "total_applications": total_applications,

        "selected_count": selected_count,

        "process_count": process_count,

        "rejected_count": rejected_count,

    }

    return render(
        request,
        "placement.html",
        context
    )

@login_required
def mocktests(request):

    return render(
        request,
        "mocktests.html"
    )

@login_required
def resume(request):

    search = request.GET.get("search", "")

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            resume = form.save(commit=False)

            resume.user = request.user

            resume.save()

            messages.success(
                request,
                "Resume uploaded successfully."
            )

            return redirect("resume")

    else:

        form = ResumeForm()

    resumes = Resume.objects.filter(
        user=request.user
    )

    if search:

        resumes = resumes.filter(
            name__icontains=search
        )

    resumes = resumes.order_by(
        "-uploaded_at"
    )

    paginator = Paginator(
        resumes,
        6
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    total_resumes = Resume.objects.filter(
        user=request.user
    ).count()

    context = {

        "form": form,

        "resumes": page_obj,

        "page_obj": page_obj,

        "search": search,

        "total_resumes": total_resumes,

    }

    return render(
        request,
        "resume.html",
        context
    )

@login_required
def interview(request):

    if request.method == "POST":

        form = InterviewSessionForm(request.POST)

        if form.is_valid():

            session = form.save(commit=False)

            session.user = request.user

            session.save()

            company_questions = {

                "Google": [

                    ("Explain Python decorators.", "Technical", "Medium"),
                    ("What are Python generators?", "Technical", "Medium"),
                    ("Explain Python GIL.", "Technical", "Hard"),
                    ("Explain Django Middleware.", "Technical", "Medium"),
                    ("Difference between Threading and Multiprocessing.", "Technical", "Hard"),
                    ("Design a URL Shortener.", "Coding", "Hard"),
                    ("Explain REST API.", "Technical", "Easy"),
                    ("How does Authentication work?", "Technical", "Medium"),
                    ("Tell me about yourself.", "HR", "Easy"),
                    ("Why Google?", "HR", "Medium"),

                ],

                "Amazon": [

                    ("Explain CAP Theorem.", "Technical", "Hard"),
                    ("Design an E-Commerce Cart.", "Coding", "Hard"),
                    ("Explain Database Indexing.", "Technical", "Medium"),
                    ("What is Redis?", "Technical", "Medium"),
                    ("Difference between SQL and NoSQL.", "Technical", "Medium"),
                    ("Explain Microservices.", "Technical", "Medium"),
                    ("REST API Best Practices.", "Technical", "Medium"),
                    ("Leadership Principle Example.", "HR", "Medium"),
                    ("Describe a difficult situation.", "HR", "Medium"),
                    ("Why Amazon?", "HR", "Easy"),

                ],

                "Microsoft": [

                    ("Explain OOP Concepts.", "Technical", "Easy"),
                    ("Difference between Process and Thread.", "Technical", "Medium"),
                    ("Explain Virtual Memory.", "Technical", "Medium"),
                    ("How does DNS work?", "Technical", "Medium"),
                    ("Explain Operating System Scheduling.", "Technical", "Hard"),
                    ("Explain REST API.", "Technical", "Easy"),
                    ("What is Git?", "Technical", "Easy"),
                    ("Tell me about your projects.", "HR", "Easy"),
                    ("Why Microsoft?", "HR", "Easy"),
                    ("Future Career Goals?", "HR", "Medium"),

                ],

                "Infosys": [

                    ("Explain OOP.", "Technical", "Easy"),
                    ("Explain DBMS.", "Technical", "Easy"),
                    ("Difference between INNER JOIN and OUTER JOIN.", "Technical", "Easy"),
                    ("Explain SDLC.", "Technical", "Easy"),
                    ("Explain Exception Handling.", "Technical", "Medium"),
                    ("Difference between List and Tuple.", "Technical", "Easy"),
                    ("What is Polymorphism?", "Technical", "Medium"),
                    ("Introduce Yourself.", "HR", "Easy"),
                    ("Strengths and Weaknesses.", "HR", "Easy"),
                    ("Why Infosys?", "HR", "Easy"),

                ],

                "TCS": [

                    ("Explain C Programming Basics.", "Technical", "Easy"),
                    ("What are Pointers?", "Technical", "Medium"),
                    ("Explain DBMS Normalization.", "Technical", "Medium"),
                    ("Difference between TCP and UDP.", "Technical", "Medium"),
                    ("Explain OSI Layers.", "Technical", "Easy"),
                    ("Explain Python Functions.", "Technical", "Easy"),
                    ("Difference between Stack and Queue.", "Technical", "Medium"),
                    ("Tell me about yourself.", "HR", "Easy"),
                    ("Why TCS?", "HR", "Easy"),
                    ("Explain your Final Year Project.", "HR", "Medium"),

                ],

                "Accenture": [

                    ("Explain Agile Methodology.", "Technical", "Easy"),
                    ("What is Scrum?", "Technical", "Medium"),
                    ("Difference between GET and POST.", "Technical", "Easy"),
                    ("Explain Git Workflow.", "Technical", "Easy"),
                    ("Explain Cloud Computing.", "Technical", "Medium"),
                    ("Difference between Authentication and Authorization.", "Technical", "Medium"),
                    ("Explain REST API.", "Technical", "Easy"),
                    ("Introduce Yourself.", "HR", "Easy"),
                    ("Leadership Experience?", "HR", "Medium"),
                    ("Why Accenture?", "HR", "Easy"),

                ],

                "Wipro": [

                    ("Explain OOP Principles.", "Technical", "Easy"),
                    ("Difference between List and Dictionary.", "Technical", "Easy"),
                    ("Explain SQL Joins.", "Technical", "Medium"),
                    ("Explain Python Functions.", "Technical", "Easy"),
                    ("What is Exception Handling?", "Technical", "Medium"),
                    ("Difference between GET and POST.", "Technical", "Easy"),
                    ("Explain REST API.", "Technical", "Medium"),
                    ("Introduce Yourself.", "HR", "Easy"),
                    ("Why Wipro?", "HR", "Easy"),
                    ("Future Goals?", "HR", "Medium"),

                ],

                "Cognizant": [

                    ("Explain DBMS.", "Technical", "Easy"),
                    ("Difference between SQL and NoSQL.", "Technical", "Medium"),
                    ("Explain Python Modules.", "Technical", "Easy"),
                    ("Explain Git.", "Technical", "Easy"),
                    ("Difference between Process and Thread.", "Technical", "Medium"),
                    ("Explain APIs.", "Technical", "Easy"),
                    ("What is Django ORM?", "Technical", "Medium"),
                    ("Introduce Yourself.", "HR", "Easy"),
                    ("Why Cognizant?", "HR", "Easy"),
                    ("Teamwork Experience?", "HR", "Medium"),

                ],

                "Capgemini": [

                    ("Explain SDLC.", "Technical", "Easy"),
                    ("Explain OOP.", "Technical", "Easy"),
                    ("Difference between Class and Object.", "Technical", "Easy"),
                    ("Explain Python Packages.", "Technical", "Medium"),
                    ("Explain Database Normalization.", "Technical", "Medium"),
                    ("Difference between Authentication and Authorization.", "Technical", "Medium"),
                    ("Explain REST API.", "Technical", "Easy"),
                    ("Tell me about yourself.", "HR", "Easy"),
                    ("Why Capgemini?", "HR", "Easy"),
                    ("Describe a challenging project.", "HR", "Medium"),

                ],

            }

            selected_questions = company_questions.get(
                session.company,
                company_questions["Google"]
            )

            for question, category, difficulty in selected_questions:

                InterviewQuestion.objects.create(

                    session=session,

                    question=question,

                    category=category,

                    difficulty=difficulty,

                )

            messages.success(

                request,

                "Mock Interview Generated Successfully."

            )

            return redirect("interview")

    else:

        form = InterviewSessionForm()

    latest_session = InterviewSession.objects.filter(

        user=request.user

    ).order_by(

        "-created_at"

    ).first()

    questions = InterviewQuestion.objects.none()

    total = 0

    completed = 0

    progress = 0

    if latest_session:

        questions = InterviewQuestion.objects.filter(

            session=latest_session

        )

        total = questions.count()

        completed = questions.filter(

            practiced=True

        ).count()

        if total > 0:

            progress = round((completed / total) * 100)

    context = {

        "form": form,

        "session": latest_session,

        "questions": questions,

        "total": total,

        "completed": completed,

        "progress": progress,

    }

    return render(

        request,

        "interview.html",

        context,

    )

@login_required
def mark_practiced(request, id):

    question = get_object_or_404(
        InterviewQuestion,
        id=id,
        session__user=request.user
    )

    question.practiced = True
    question.save()

    messages.success(
        request,
        "Question marked as practiced."
    )

    return redirect("interview")

@login_required
def calendar(request):

    events = Event.objects.filter(
        user=request.user
    ).order_by(
        "event_date",
        "event_time"
    )

    upcoming_events = events.filter(
        event_date__gte=date.today()
    )

    context = {

        "events": events,

        "upcoming_events": upcoming_events,

        "today": date.today(),

    }

    return render(
        request,
        "calendar.html",
        context
    )

@login_required
def add_event(request):

    if request.method == "POST":

        form = EventForm(request.POST)

        if form.is_valid():

            event = form.save(commit=False)

            event.user = request.user

            event.save()

            messages.success(
                request,
                "Event added successfully."
            )

            return redirect("calendar")

    else:

        form = EventForm()

    return render(
        request,
        "add_event.html",
        {
            "form": form
        }
    )

@login_required
def edit_event(request, id):

    event = get_object_or_404(
        Event,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = EventForm(
            request.POST,
            instance=event
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Event updated successfully."
            )

            return redirect("calendar")

    else:

        form = EventForm(
            instance=event
        )

    return render(
        request,
        "edit_event.html",
        {
            "form": form,
            "event": event
        }
    )


@login_required
def delete_event(request, id):

    event = get_object_or_404(
        Event,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        event.delete()

        messages.success(
            request,
            "Event deleted successfully."
        )

        return redirect("calendar")

    return render(
        request,
        "delete_event.html",
        {
            "event": event
        }
    )


@login_required
def ai_study_planner(request):

    if request.method == "POST":

        form = StudyPlanForm(request.POST)

        if form.is_valid():

            plan = form.save(commit=False)

            plan.user = request.user

            plan.save()

            messages.success(
                request,
                "AI Study Plan Generated Successfully."
            )

            return redirect("ai_study_planner")

    else:

        form = StudyPlanForm()

    plan = StudyPlan.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    topics = Topic.objects.filter(
        subject__user=request.user,
        status="Pending"
    ).order_by(
        "difficulty",
        "estimated_hours"
    )

    # -----------------------
    # AI Today's Recommendation
    # -----------------------

    recommended_topics = []

    if topics.exists():

        hard_topics = topics.filter(
            difficulty="Hard"
        ).order_by("-estimated_hours")

        medium_topics = topics.filter(
            difficulty="Medium"
        ).order_by("-estimated_hours")

        easy_topics = topics.filter(
            difficulty="Easy"
        ).order_by("-estimated_hours")

        recommended_topics = list(hard_topics) + \
                             list(medium_topics) + \
                             list(easy_topics)

        recommended_topics = recommended_topics[:3]

    # -----------------------
    # AI Schedule
    # -----------------------

    schedule = []

    if plan:

        current_day = date.today()

        daily_hours = plan.study_hours

        remaining_hours = daily_hours

        day_topics = []

        for topic in topics:

            if topic.estimated_hours <= remaining_hours:

                day_topics.append(topic)

                remaining_hours -= topic.estimated_hours

            else:

                schedule.append({

                    "date": current_day,

                    "topics": day_topics,

                })

                current_day += timedelta(days=1)

                day_topics = [topic]

                remaining_hours = daily_hours - topic.estimated_hours

        if day_topics:

            schedule.append({

                "date": current_day,

                "topics": day_topics,

            })

    # -----------------------
    # Statistics
    # -----------------------

    total_topics = Topic.objects.filter(
        subject__user=request.user
    ).count()

    completed_topics = Topic.objects.filter(
        subject__user=request.user,
        status="Completed"
    ).count()

    pending_topics = Topic.objects.filter(
        subject__user=request.user,
        status="Pending"
    ).count()

    if total_topics > 0:

        progress = int(
            (completed_topics / total_topics) * 100
        )

    else:

        progress = 0

    estimated_days = len(schedule)

    warning = False

    days_left = None

    if plan:

        days_left = (
            plan.exam_date - date.today()
        ).days

        if days_left >= 0 and estimated_days > days_left:

            warning = True

    context = {

        "form": form,

        "plan": plan,

        "schedule": schedule,

        "progress": progress,

        "completed_topics": completed_topics,

        "pending_topics": pending_topics,

        "estimated_days": estimated_days,

        "days_left": days_left,

        "warning": warning,

        "recommended_topics": recommended_topics,

    }

    return render(

        request,

        "ai_study_planner.html",

        context

    )

@login_required
def placement_readiness(request):

    profile = Profile.objects.filter(
        user=request.user
    ).first()

    resumes = Resume.objects.filter(
        user=request.user
    ).count()

    companies = Company.objects.filter(
        user=request.user
    ).count()

    events = Event.objects.filter(
        user=request.user
    ).count()

    total_topics = Topic.objects.filter(
        subject__user=request.user
    ).count()

    completed_topics = Topic.objects.filter(
        subject__user=request.user,
        status="Completed"
    ).count()

    score = 0

    # -------------------------
    # Profile
    # -------------------------

    profile_complete = False

    if profile:

        if (

            profile.full_name and
            profile.phone and
            profile.college and
            profile.degree and
            profile.graduation_year

        ):

            score += 20

            profile_complete = True

    # -------------------------
    # Resume
    # -------------------------

    if resumes > 0:

        score += 20

    # -------------------------
    # Study Progress
    # -------------------------

    study_progress = 0

    if total_topics > 0:

        study_progress = int(
            (completed_topics / total_topics) * 100
        )

        score += int(study_progress * 0.30)

    # -------------------------
    # Companies
    # -------------------------

    if companies >= 5:

        score += 20

    elif companies > 0:

        score += 10

    # -------------------------
    # Calendar
    # -------------------------

    if events >= 3:

        score += 10

    elif events > 0:

        score += 5

    context = {

        "score": score,

        "profile_complete": profile_complete,

        "resume_count": resumes,

        "study_progress": study_progress,

        "companies": companies,

        "events": events,

    }

    return render(

        request,

        "placement_readiness.html",

        context

    )

@login_required
def analytics(request):

    subjects = Subject.objects.filter(
        user=request.user
    )

    topics = Topic.objects.filter(
        subject__user=request.user
    )

    companies = Company.objects.filter(
        user=request.user
    )

    resumes = Resume.objects.filter(
        user=request.user
    )

    # Subject-wise topic count
    subject_labels = []
    subject_topic_count = []

    for subject in subjects:

        subject_labels.append(subject.name)

        subject_topic_count.append(
            subject.topics.count()
        )

    # Placement Status
    placement_labels = [
        "Applied",
        "OA",
        "Technical",
        "HR",
        "Selected",
        "Rejected",
    ]

    placement_data = [

        companies.filter(status="Applied").count(),

        companies.filter(status="OA").count(),

        companies.filter(status="Technical").count(),

        companies.filter(status="HR").count(),

        companies.filter(status="Selected").count(),

        companies.filter(status="Rejected").count(),

    ]

    context = {

        # Dashboard Cards

        "subject_count": subjects.count(),

        "topic_count": topics.count(),

        "resume_count": resumes.count(),

        # Topics

        "completed_topics": topics.filter(
            status="Completed"
        ).count(),

        "pending_topics": topics.filter(
            status="Pending"
        ).count(),

        "progress_topics": topics.filter(
            status="In Progress"
        ).count(),

        # Placement

        "applied": companies.filter(
            status="Applied"
        ).count(),

        "oa": companies.filter(
            status="OA"
        ).count(),

        "technical": companies.filter(
            status="Technical"
        ).count(),

        "hr": companies.filter(
            status="HR"
        ).count(),

        "selected": companies.filter(
            status="Selected"
        ).count(),

        "rejected": companies.filter(
            status="Rejected"
        ).count(),

        # Chart Data

        "subject_labels": subject_labels,

        "subject_topic_count": subject_topic_count,

        "placement_labels": placement_labels,

        "placement_data": placement_data,

    }

    return render(
        request,
        "analytics.html",
        context
    )

@login_required
def settings(request):

    settings_obj, created = UserSettings.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = UserSettingsForm(
            request.POST,
            instance=settings_obj
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Settings updated successfully."
            )

            return redirect("settings")

    else:

        form = UserSettingsForm(
            instance=settings_obj
        )

    context = {

        "form": form,

        "settings_obj": settings_obj,

    }

    return render(
        request,
        "settings.html",
        context
    )

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("login")

    else:

        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            username = form.cleaned_data.get("username")

            password = form.cleaned_data.get("password")

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                login(request, user)

                return redirect("dashboard")

    else:

        form = AuthenticationForm()

    return render(
        request,
        "registration/login.html",
        {
            "form": form
        }
    )

def logout_view(request):

    logout(request)

    return redirect("login")

@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )

@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("profile")

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        "edit_profile.html",
        {
            "form": form
        }
    )

@login_required
def edit_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = SubjectForm(
            request.POST,
            instance=subject
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Subject updated successfully."
            )

            return redirect("subjects")

    else:

        form = SubjectForm(
            instance=subject
        )

    context = {

        "form": form,

        "subject": subject

    }

    return render(
        request,
        "edit_subject.html",
        context
    )

@login_required
def delete_subject(request, id):

    subject = get_object_or_404(
        Subject,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        subject.delete()

        messages.success(
            request,
            "Subject deleted successfully."
        )

        return redirect("subjects")

    return render(
        request,
        "delete_subject.html",
        {
            "subject": subject
        }
    ) 


@login_required
def add_company(request):

    if request.method == "POST":

        form = CompanyForm(request.POST)

        if form.is_valid():

            company = form.save(commit=False)

            company.user = request.user

            company.save()

            messages.success(
                request,
                "Company added successfully."
            )

            return redirect("placement")

    else:

        form = CompanyForm()

    context = {

        "form": form,

    }

    return render(
        request,
        "add_company.html",
        context
    )

@login_required
def edit_company(request, id):

    company = get_object_or_404(
        Company,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = CompanyForm(
            request.POST,
            instance=company
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Company updated successfully."
            )

            return redirect("placement")

    else:

        form = CompanyForm(
            instance=company
        )

    return render(
    request,
    "edit_company.html",
    {
        "form": form,
        "company": company,
    }
)


@login_required
def delete_company(request, id):

    company = get_object_or_404(
        Company,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        company.delete()

        messages.success(
            request,
            "Company deleted successfully."
        )

        return redirect("placement")

    return render(
        request,
        "delete_company.html",
        {
            "company": company
        }
    )

@login_required
def delete_resume(request, id):

    resume = get_object_or_404(
        Resume,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        resume.delete()

        messages.success(
            request,
            "Resume deleted successfully."
        )

        return redirect("resume")

    return render(
        request,
        "delete_resume.html",
        {
            "resume": resume
        }
    )

@login_required
def edit_resume(request, id):

    resume = get_object_or_404(
        Resume,
        id=id,
        user=request.user
    )

    if request.method == "POST":

        form = ResumeForm(
            request.POST,
            request.FILES,
            instance=resume
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Resume updated successfully."
            )

            return redirect("resume")

    else:

        form = ResumeForm(
            instance=resume
        )

    return render(
        request,
        "edit_resume.html",
        {
            "form": form,
            "resume": resume
        }
    )