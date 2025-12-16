from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from .form import LoginForm
from .models import Essay
from .utils import check_essay
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet

User = get_user_model()



@login_required

def admin_users(request):
    users = User.objects.all()
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        identydoc = request.FILES.get("identydoc")
        dob = request.POST.get("DOB")
        is_active = bool(request.POST.get("is_active"))
        is_staff = bool(request.POST.get("is_staff"))
        is_superuser = bool(request.POST.get("is_superuser"))

        if password != password2:
            messages.error(request, "Passwords do not match")
        else:
            User.objects.create_user(
                username=username,
                password=password,
                identydoc=identydoc,
                DOB=dob,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            messages.success(request, "User created successfully")
            return redirect("admin_users")

    return render(request, "admin/users.html", {"users": users})

@login_required
def admin_essays(request):
    essays = Essay.objects.select_related('user').order_by('-created_at')
    return render(request, "admin/essays.html", {"essays": essays})


# -------------------------------
# Decorators
# -------------------------------
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper

# -------------------------------
# Admin Views
# -------------------------------
@login_required
@admin_required
def admin_dashboard(request):
    if request.method == "POST":
        # Add new user
        username = request.POST['username']
        password1 = request.POST['password']
        password2 = request.POST['password2']
        if password1 != password2:
            messages.error(request, "Passwords do not match")
        else:
            user = User.objects.create_user(
                username=username,
                password=password1,
                is_active='is_active' in request.POST,
                is_staff='is_staff' in request.POST,
                is_superuser='is_superuser' in request.POST,
            )
            if 'DOB' in request.POST and request.POST['DOB']:
                user.DOB = request.POST['DOB']
            if 'identydoc' in request.FILES:
                user.identydoc = request.FILES['identydoc']
            user.save()
            messages.success(request, f"User {username} created successfully")
            return redirect('admin_dashboard')

    users = User.objects.all()
    essays = Essay.objects.select_related('user').order_by('-created_at')

    context = {
        'users_count': users.count(),
        'essays_count': essays.count(),
        'approved_count': Essay.objects.filter(is_approved=True).count(),
        'rejected_count': Essay.objects.filter(is_rejected=True).count(),
        'users': users,
        'essays': essays,
    }
    return render(request, 'admin/admin_dashboard.html', context)


@login_required
@admin_required
def approve_essay(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id)
    essay.is_approved = True
    essay.is_rejected = False
    essay.save()
    messages.success(request, f"Essay '{essay.title}' approved.")
    return redirect('admin_dashboard')


@login_required
@admin_required
def reject_essay(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id)
    essay.is_approved = False
    essay.is_rejected = True
    essay.save()
    messages.success(request, f"Essay '{essay.title}' rejected.")
    return redirect('admin_dashboard')


@login_required
@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent deleting yourself
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('admin_dashboard')

    if request.method == "POST":
        username = user.username
        user.delete()
        messages.success(request, f"User '{username}' deleted successfully.")

    return redirect('admin_dashboard')


@login_required
@admin_required
def delete_essay(request, essay_id):
    essay = get_object_or_404(Essay, id=essay_id)

    if request.method == "POST":
        title = essay.title
        essay.delete()
        messages.success(request, f"Essay '{title}' deleted successfully.")

    return redirect('admin_dashboard')




# -------------------------------
# Authentication Views
# -------------------------------
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember_me')

            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                if user.is_superuser:
                    return redirect('admin_dashboard')
                return redirect('essay')
            else:
                if User.objects.filter(username=username).exists():
                    form.add_error('password', "Incorrect password.")
                else:
                    form.add_error('username', "Username does not exist.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')

# -------------------------------
# User Views
# -------------------------------
def home_view(request):
    return render(request, 'home.html')


@login_required
def essay_view(request):
    return render(request, 'essay.html')


@login_required
def submit_essay(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        grammar_errors, spelling_errors = check_essay(content)
        total_errors = grammar_errors + spelling_errors
        total_words = len(content.split())
        score = max(0, 100 - (total_errors * 2)) if total_words > 0 else 0

        # Save PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = [Paragraph(f"<b>Title:</b> {title}", styles["Normal"]),
                 Paragraph(f"<b>Author:</b> {request.user.username}", styles["Normal"]),
                 Spacer(1, 12)]
        for para in content.split("\n"):
            story.append(Paragraph(para, styles["Normal"]))
            story.append(Spacer(1, 6))
        doc.build(story)
        pdf_file = ContentFile(buffer.getvalue(), name=f"{title}.pdf")
        buffer.close()

        Essay.objects.create(
            user=request.user,
            title=title,
            content=content,
            grammar_errors=grammar_errors,
            spelling_errors=spelling_errors,
            total_errors=total_errors,
            score=score,
            pdf_file=pdf_file,
            is_approved=False,
            is_rejected=False
        )

        return redirect("home")

    return render(request, "essay.html")


def leaderboard(request):
    essays = Essay.objects.filter(is_approved=True).order_by('-score', 'total_errors', 'created_at')
    return render(request, "leaderboard.html", {"essays": essays})
