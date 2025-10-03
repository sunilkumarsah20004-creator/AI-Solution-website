from django.utils.text import slugify
import uuid


def generate_slug(title: str, class_name: str) -> str:
    title = slugify(title)
    while class_name.objects.filter(slug=title).exists():
        title = f"{title}-{uuid.uuid4().hex[:4]}"
    return title
