# app/models.py
from django.db import models
from django.db.models import Q, F
from django.contrib.auth import get_user_model
from django.utils import timezone
from .utils import generate_slug
from django.urls import reverse

User = get_user_model()


# ---------- Common mixins ----------
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---------- Choices / Enums ----------
class ArticleStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    PUBLISHED = "published", "Published"
    ARCHIVED = "archived", "Archived"


class InquiryStatus(models.TextChoices):
    NEW = "new", "New"
    IN_REVIEW = "in_review", "In review"
    CLOSED = "closed", "Closed"


class SenderType(models.TextChoices):
    ADMIN = "admin", "Admin"
    CUSTOMER = "customer", "Customer"


class Direction(models.TextChoices):
    INBOUND = "inbound", "Inbound"
    OUTBOUND = "outbound", "Outbound"


class ServiceStatus(models.TextChoices):
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    COMING_SOON = "coming_soon", "Coming Soon"


class ServiceCategory(models.TextChoices):
    AI_CONSULTING = "ai_consulting", "AI Strategy & Consulting"
    ML_DEVELOPMENT = "ml_development", "Machine Learning Development"
    NLP = "nlp", "Natural Language Processing"
    COMPUTER_VISION = "computer_vision", "Computer Vision"
    AI_INTEGRATION = "ai_integration", "AI Integration & Deployment"
    DATA_ANALYTICS = "data_analytics", "Advanced Data Analytics"


# ---------- Core tables ----------
# software solution

class SoftwareSolution(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    image = models.ImageField(
        upload_to="software_solutions/", blank=True, null=True)
    description = models.TextField(blank=True)  # describe the system
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(User, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="solutions")

    class Meta:
        indexes = [models.Index(fields=["slug"])]
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, SoftwareSolution)
        super().save(*args, **kwargs)


# service
class Service(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    description = models.TextField()
    short_description = models.TextField(max_length=500, blank=True)
    category = models.CharField(
        max_length=50, choices=ServiceCategory.choices, db_index=True
    )
    status = models.CharField(
        max_length=20, choices=ServiceStatus.choices, default=ServiceStatus.ACTIVE, db_index=True
    )
    icon = models.CharField(max_length=100, blank=True)  # For Remix icon class names
    image = models.ImageField(upload_to="services/", blank=True, null=True)
    features = models.JSONField(default=list, blank=True)  # List of feature strings
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="services"
    )

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["category", "status"]),
        ]
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, Service)
        super().save(*args, **kwargs)


# case study
class CaseStudy(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    summary = models.TextField(blank=True)      # short overview
    problem = models.TextField(blank=True)
    solution = models.TextField(blank=True)
    results = models.TextField(blank=True)

    client_name = models.CharField(max_length=255, blank=True)
    client_company = models.CharField(max_length=255, blank=True)
    client_job_title = models.CharField(max_length=255, blank=True)

    image = models.ImageField(upload_to="case_studies/", blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    created_by = models.ForeignKey(User, null=True, blank=True,
                                   on_delete=models.SET_NULL, related_name="case_studies")

    # Optional: link to one or more solutions
    solutions = models.ManyToManyField(
        SoftwareSolution, blank=True, related_name="case_studies")

    class Meta:
        indexes = [models.Index(fields=["slug"])]
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, CaseStudy)
        super().save(*args, **kwargs)


# article
class Article(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    content = models.TextField()
    excerpt = models.TextField(blank=True)
    status = models.CharField(
        max_length=16, choices=ArticleStatus.choices, default=ArticleStatus.DRAFT, db_index=True
    )
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    published_at = models.DateTimeField(null=True, blank=True, db_index=True)
    author = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="articles"
    )

    class Meta:
        indexes = [
            models.Index(fields=["status", "-published_at"]),
        ]
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Auto-slug if empty
        if not self.slug:
            self.slug = generate_slug(self.title, Article)
        super().save(*args, **kwargs)

# event

class Event(TimeStampedModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_public = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL, related_name="events")

    class Meta:
        indexes = [
            models.Index(fields=["is_public", "starts_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="event_ends_after_start",
                check=Q(ends_at__isnull=True) | Q(ends_at__gte=F("starts_at")),
            )
        ]
        ordering = ["starts_at", "id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_slug(self.title, Event)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# event gallery image
class EventGalleryImage(TimeStampedModel):
    """
    Stores images for the event gallery. Multiple images can be associated with a single event.
    """
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ImageField(upload_to="event_gallery/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower numbers appear first)")

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["event", "order"]),
        ]

    def __str__(self):
        return f"{self.event.title} - Image {self.id}"


# inquiry
class Inquiry(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company_name = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=255, blank=True)
    job_details = models.TextField(blank=True)
    status = models.CharField(
        max_length=16, choices=InquiryStatus.choices, default=InquiryStatus.NEW, db_index=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["email"]),
        ]
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.name} ({self.email})"


# inquiry response
class InquiryResponse(models.Model):
    """
    Stores a threaded message/reply or internal note tied to an Inquiry.
    - If sender_type='admin', 'admin' must be set.
    - direction: inbound (from customer) or outbound (to customer).
    """
    inquiry = models.ForeignKey(
        Inquiry, on_delete=models.CASCADE, related_name="responses")
    sender_type = models.CharField(max_length=16, choices=SenderType.choices)
    admin = models.ForeignKey(User, null=True, blank=True,
                              on_delete=models.SET_NULL, related_name="inquiry_responses")
    recipient = models.CharField(
        max_length=255, blank=True)  # e.g., customer email
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    direction = models.CharField(
        max_length=16, choices=Direction.choices, default=Direction.OUTBOUND)
    sent_at = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["inquiry", "sent_at"]),
            models.Index(fields=["sender_type"]),
            models.Index(fields=["direction"]),
        ]
        ordering = ["sent_at", "id"]
        constraints = [
            # If sender is admin, admin FK must be present
            models.CheckConstraint(
                name="inquiry_resp_admin_required_when_admin_sender",
                check=Q(sender_type=SenderType.CUSTOMER) | (
                    Q(sender_type=SenderType.ADMIN) & Q(admin__isnull=False)),
            )
        ]

    def __str__(self):
        who = self.admin.get_username() if (self.admin and self.sender_type ==
                                            SenderType.ADMIN) else self.sender_type
        return f"Resp[{self.inquiry_id}] {who}: {self.subject or self.body[:30]}"
