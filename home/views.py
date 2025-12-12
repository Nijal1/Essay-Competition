from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .form import LoginForm

from django.contrib.auth.decorators import login_required
from .models import Essay
from .utils import check_essay
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

User = get_user_model()

# Home page
def home_view(request):
    return render(request, 'home.html')


# Essay page
def essay_view(request):
    return render(request, 'essay.html')


# Login view
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember = form.cleaned_data.get('remember_me')

            # Authenticate user
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)  # Session expires on browser close
                return redirect("essay")
            else:
                # Determine if username exists
                if User.objects.filter(username=username).exists():
                    form.add_error('password', "Incorrect password.")
                else:
                    form.add_error('username', "Username does not exist.")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


# Logout view
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')





@login_required
def submit_essay(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        grammar_errors, spelling_errors = check_essay(content)
        total_errors = grammar_errors + spelling_errors
        total_words = len(content.split())
        score = max(0, 100 - (total_errors * 2)) if total_words > 0 else 0

        # Save PDF in media/essays/pdfs
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph(f"<b>Title:</b> {title}", styles["Normal"]))
        story.append(Paragraph(f"<b>Author:</b> {request.user.username}", styles["Normal"]))
        story.append(Spacer(1, 12))

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
            is_approved=False,  # User cannot see it yet
            is_rejected=False
        )

        return redirect("home")

    return render(request, "essay.html")




def leaderboard(request):
    # Only show approved essays to users
    essays = Essay.objects.filter(is_approved=True).order_by('-score', 'total_errors', 'created_at')
    return render(request, "leaderboard.html", {"essays": essays})


