from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db.models import Count
from django.core.paginator import Paginator
from .models import Inquiry, CaseStudy, Article, Event, Service
from django.contrib import messages
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.messages import get_messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .utils import generate_gemini_response
from django.utils import timezone
import json
import logging

logger = logging.getLogger(__name__)
# Phone number validator
phone_validator = RegexValidator(
    regex=r'^\+?[0-9\-\s()]{7,20}$',
    message="Enter a valid phone number with country code (e.g. +977-9812345678)."
)


def generate_toasts_from_messages(request):
    """
    Generate simple toast data from Django messages.
    """
    COLOR_MAP = {
        "success": "green",
        "error": "red",
        "warning": "yellow",
        "info": "blue",
    }

    toasts = []
    for m in get_messages(request):
        color = COLOR_MAP.get(getattr(m, "level_tag", ""), "gray")
        toasts.append({
            "text": str(m.message),
            "color": color,
        })
    return toasts

# handle inquiry submission


def send_auto_reply(customer_email, name):
    context = {
        "name": name,
        "year": timezone.now().year,
    }

    subject = "Thanks for contacting AI-Solutions"
    text_body = render_to_string("base/components/email/reply.txt", context)
    html_body = render_to_string("base/components/email/reply.html", context)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email="support@ai-solutions.com",
        to=[customer_email],
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


def handle_inquiry_submission(request):
    """Handles POST inquiry submission logic."""
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    phone = request.POST.get("phone", "").strip()
    company_name = request.POST.get("company_name", "").strip()
    country = request.POST.get("country", "").strip()
    job_title = request.POST.get("job_title", "").strip()
    job_details = request.POST.get("job_details", "").strip()

    # Check required fields (only name and email are required per model)
    if not name:
        messages.error(request, "Please enter your name")
        return False

    if not email:
        messages.error(request, "Please enter your email address")
        return False

    # Validate phone number only if provided
    if phone:
        try:
            phone_validator(phone)
        except ValidationError:
            messages.error(
                request, "Enter a valid phone number with country code (e.g. +977-9812345678)")
            return False

    try:
        # Save inquiry
        Inquiry.objects.create(
            name=name,
            email=email,
            phone=phone,
            company_name=company_name,
            country=country,
            job_title=job_title,
            job_details=job_details,
        )
        # send reply to the customer
        send_auto_reply(email, name)
        messages.success(
            request, "Thank you! Your inquiry has been submitted successfully. We'll respond within 24 hours.")
        return True

    except Exception as e:
        messages.error(request, "Something went wrong. Please try again.")
        return False


def home(request):
    case_studies = CaseStudy.objects.all()[:3]
    articles = Article.objects.filter(status='published')[:3]
    events = Event.objects.all()[:6]

    context = {
        "case_studies": case_studies,
        "articles": articles,
        "events": events,
    }
    return render(request, "base/pages/index.html", context)




def articles_page(request):
    articles = Article.objects.filter(status='published').order_by('-published_at')
    context = {
        "articles": articles,
    }
    return render(request, "base/pages/articles.html", context)



def articles_details(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        return render(request, "base/pages/articles-details.html", {"article": article})
    except Article.DoesNotExist:
        from django.http import Http404
        raise Http404("Article not found")




def all_events_page(request):
    events = Event.objects.all().order_by('starts_at')
    return render(request, "base/pages/events.html", {"events": events})


def events_details(request, slug):
    try:
        event = Event.objects.get(slug=slug)
        return render(request, "base/pages/events-details.html", {"event": event})
    except Event.DoesNotExist:
        from django.http import Http404
        raise Http404("Event not found")




def case_study_list(request):
    case_studies = CaseStudy.objects.all()

    context = {
        "case_studies": case_studies,
    }
    return render(request, "base/pages/case-study.html", context)


def case_studies_details(request, slug):
    try:
        case_study = CaseStudy.objects.get(slug=slug)
        return render(request, "base/pages/case-studies-details.html", {"case_study": case_study})
    except CaseStudy.DoesNotExist:
        from django.http import Http404
        raise Http404("Case study not found")

def services(request):
    """Services page view"""
    from .models import Service

    # Get all active services, ordered by title
    services = Service.objects.filter(status='active').order_by('title')

    context = {
        'services': services,
    }
    return render(request, "base/pages/services.html", context)

def contact(request):
    if request.method == "POST":
        handle_inquiry_submission(request)
        return redirect("contact")

    context = {
        "toasts": generate_toasts_from_messages(request)
    }
    return render(request, "base/pages/contacts.html", context=context)




# --------------------- Django View ---------------------
def ai_assistant(request):
    """AI Assistant chatbot page view with Gemini integration"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({
                    'response': 'Please enter a message.',
                    'is_html': False
                }, status=400)

            # Generate AI response using Gemini
            response = generate_gemini_response(user_message)

            return JsonResponse({
                'response': response,
                'is_html': True
            })
        except Exception as e:
            logger.error(f"Error in ai_assistant view: {str(e)}")
            return JsonResponse({
                'response': 'Sorry, I encountered an error. Please try again.',
                'is_html': False
            }, status=500)

    return render(request, "base/pages/ai-assistant.html")
