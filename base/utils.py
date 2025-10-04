import uuid
import os
import json
import logging
from django.utils.text import slugify
from django.http import JsonResponse
from django.shortcuts import render
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

# --------------------- Slug Generator ---------------------
def generate_slug(title: str, class_name) -> str:
    """Generate unique slug for a model instance"""
    title = slugify(title)
    while class_name.objects.filter(slug=title).exists():
        title = f"{title}-{uuid.uuid4().hex[:4]}"
    return title


# --------------------- Company Context ---------------------
def get_company_context():
    """Fetch company data from database for AI context"""
    # Import here to avoid circular import
    from .models import Service, CaseStudy

    # Get services
    services = Service.objects.filter(status="active")[:6]
    services_info = "\n".join(
        [f"- {s.title}: {s.short_description}" for s in services]
    ) if services.exists() else "AI/ML Services, NLP Solutions, Computer Vision"

    # Get case studies
    case_studies = CaseStudy.objects.all()[:3]
    case_studies_info = "\n".join(
        [f"- {cs.title}: {cs.summary}" for cs in case_studies]
    ) if case_studies.exists() else "Multiple successful AI implementation projects"

    return f"""
SERVICES WE OFFER:
{services_info}

SUCCESS STORIES:
{case_studies_info}

CONTACT INFORMATION:
- Website: Visit /contact/ page for inquiry form
- Services Page: /services/
- Case Studies: /case-study/
- Articles: /articles/
- Events: /events/
"""


# --------------------- Simple Chatbot Response ---------------------
def generate_gemini_response(query: str) -> str:
    """
    Simple rule-based chatbot for AI Solutions company.
    No external API needed - just pattern matching and responses.
    """
    # Import here to avoid circular import
    from .models import Service, CaseStudy

    query_lower = query.lower().strip()

    # Get company data
    try:
        services = Service.objects.filter(status="active")
        case_studies = CaseStudy.objects.all()[:3]
    except:
        services = []
        case_studies = []

    # Keywords for pattern matching
    service_keywords = ['service', 'services', 'offer', 'provide', 'do', 'help', 'solutions']
    pricing_keywords = ['price', 'cost', 'pricing', 'charge', 'fee', 'payment']
    about_keywords = ['about', 'company', 'who', 'what is', 'tell me']
    contact_keywords = ['contact', 'reach', 'talk', 'speak', 'email', 'phone', 'call']
    case_study_keywords = ['case study', 'case studies', 'portfolio', 'project', 'work', 'clients', 'success']
    ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'nlp', 'computer vision']

    # Pattern matching responses

    # Greetings
    if any(word in query_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return """
        <p>Hello! 👋 Welcome to <strong>AI Solutions</strong>!</p>
        <p>I'm here to help you learn about our AI services and how we can transform your business with artificial intelligence.</p>
        <br/>
        <p>You can ask me about:</p>
        <ul class="list-disc list-inside mt-2 space-y-1">
            <li>Our AI services and solutions</li>
            <li>Case studies and success stories</li>
            <li>How to get in touch with our team</li>
        </ul>
        """

    # Services
    if any(keyword in query_lower for keyword in service_keywords):
        if services:
            services_html = "<ul class='list-disc list-inside mt-2 space-y-2'>"
            for service in services[:6]:
                services_html += f"<li><strong>{service.title}</strong>: {service.short_description}</li>"
            services_html += "</ul>"

            return f"""
            <p>At <strong>AI Solutions</strong>, we offer comprehensive AI services:</p>
            {services_html}
            <br/>
            <p>Visit our <a href="/services/" class="text-emerald-400 underline">Services page</a> for detailed information or <a href="/contact/" class="text-emerald-400 underline">contact us</a> to discuss your project!</p>
            """
        else:
            return """
            <p>We offer a wide range of <strong>AI solutions</strong> including:</p>
            <ul class="list-disc list-inside mt-2 space-y-1">
                <li>AI Strategy & Consulting</li>
                <li>Machine Learning Development</li>
                <li>Natural Language Processing</li>
                <li>Computer Vision Solutions</li>
                <li>AI Integration & Deployment</li>
            </ul>
            <br/>
            <p>Visit our <a href="/services/" class="text-emerald-400 underline">Services page</a> or <a href="/contact/" class="text-emerald-400 underline">contact us</a> to learn more!</p>
            """

    # Pricing
    if any(keyword in query_lower for keyword in pricing_keywords):
        return """
        <p>Our pricing is <strong>customized</strong> based on your specific needs and project scope.</p>
        <br/>
        <p>Factors we consider:</p>
        <ul class="list-disc list-inside mt-2 space-y-1">
            <li>Project complexity and requirements</li>
            <li>Timeline and deliverables</li>
            <li>Ongoing support needs</li>
        </ul>
        <br/>
        <p>Please <a href="/contact/" class="text-emerald-400 underline">contact our team</a> for a personalized quote!</p>
        """

    # About company
    if any(keyword in query_lower for keyword in about_keywords):
        return """
        <p><strong>AI Solutions</strong> is a leading AI development company specializing in custom artificial intelligence solutions for businesses.</p>
        <br/>
        <p>We help organizations:</p>
        <ul class="list-disc list-inside mt-2 space-y-1">
            <li>Solve complex problems with AI</li>
            <li>Automate processes and increase efficiency</li>
            <li>Gain insights from data</li>
            <li>Build competitive advantages with AI technology</li>
        </ul>
        <br/>
        <p>Explore our <a href="/services/" class="text-emerald-400 underline">Services</a> or <a href="/case-study/" class="text-emerald-400 underline">Case Studies</a> to see what we can do for you!</p>
        """

    # Contact
    if any(keyword in query_lower for keyword in contact_keywords):
        return """
        <p>We'd love to hear from you! 💬</p>
        <br/>
        <p>You can reach us through our <a href="/contact/" class="text-emerald-400 underline">Contact page</a> where you can:</p>
        <ul class="list-disc list-inside mt-2 space-y-1">
            <li>Fill out an inquiry form</li>
            <li>Tell us about your project</li>
            <li>Get a response within 24 hours</li>
        </ul>
        <br/>
        <p><a href="/contact/" class="text-emerald-400 underline">Contact us now</a> to get started!</p>
        """

    # Case studies
    if any(keyword in query_lower for keyword in case_study_keywords):
        if case_studies:
            cs_html = "<ul class='list-disc list-inside mt-2 space-y-2'>"
            for cs in case_studies:
                cs_html += f"<li><strong>{cs.title}</strong>: {cs.summary[:100]}...</li>"
            cs_html += "</ul>"

            return f"""
            <p>We're proud of our successful AI implementations! Here are some highlights:</p>
            {cs_html}
            <br/>
            <p>See all our success stories on our <a href="/case-study/" class="text-emerald-400 underline">Case Studies page</a>!</p>
            """
        else:
            return """
            <p>We've helped numerous companies transform their businesses with AI! 🚀</p>
            <br/>
            <p>Check out our <a href="/case-study/" class="text-emerald-400 underline">Case Studies page</a> to see our successful projects and client testimonials.</p>
            """

    # AI-related general questions
    if any(keyword in query_lower for keyword in ai_keywords):
        return """
        <p>Artificial Intelligence is transforming businesses across industries! 🤖</p>
        <br/>
        <p>At <strong>AI Solutions</strong>, we specialize in:</p>
        <ul class="list-disc list-inside mt-2 space-y-1">
            <li><strong>Machine Learning</strong> - Predictive analytics and automation</li>
            <li><strong>Natural Language Processing</strong> - Chatbots and text analysis</li>
            <li><strong>Computer Vision</strong> - Image recognition and processing</li>
            <li><strong>AI Strategy</strong> - Planning and implementation guidance</li>
        </ul>
        <br/>
        <p>Explore our <a href="/services/" class="text-emerald-400 underline">Services</a> or <a href="/contact/" class="text-emerald-400 underline">contact us</a> to discuss your AI needs!</p>
        """

    # Default response
    return """
    <p>I'm here to help you learn about <strong>AI Solutions</strong>! 🤝</p>
    <br/>
    <p>I can answer questions about:</p>
    <ul class="list-disc list-inside mt-2 space-y-1">
        <li>Our <a href="/services/" class="text-emerald-400 underline">AI Services</a></li>
        <li>Our <a href="/case-study/" class="text-emerald-400 underline">Case Studies</a></li>
        <li>How to <a href="/contact/" class="text-emerald-400 underline">Contact us</a></li>
        <li>Our <a href="/articles/" class="text-emerald-400 underline">Articles</a> and insights</li>
        <li>Upcoming <a href="/events/" class="text-emerald-400 underline">Events</a></li>
    </ul>
    <br/>
    <p>What would you like to know?</p>
    """
