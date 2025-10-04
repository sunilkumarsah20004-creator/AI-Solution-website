from django.contrib import admin
from .models import Article, Event, EventGalleryImage, Inquiry, InquiryResponse, SoftwareSolution, CaseStudy, Service


# software solution
class SoftwareSolutionAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'slug', 'description',
        'published_at', 'created_by',
    )
    list_filter = ('title', 'created_by')
    search_fields = ('title', 'published_at')
    exclude = ("created_by",)
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)

# case study
class CaseStudyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'summary', 'problem', 'solution', 'results', 'client_name', 'client_company', 'client_job_title', 'image', 'published_at', 'created_by')
    list_filter = ('title', 'published_at', 'created_by')
    search_fields = ('title', 'summary', 'problem', 'solution', 'results', 'client_name', 'client_company', 'client_job_title')
    exclude = ("created_by",)
    prepopulated_fields = {"slug": ("title",)}

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


# service
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'status', 'created_at'
    )
    list_filter = ('category', 'status', 'created_at')
    search_fields = ('title', 'description', 'short_description')
    list_editable = ('status',)
    exclude = ("created_by",)
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description')
        }),
        ('Categorization', {
            'fields': ('category', 'status')
        }),
        ('Visual', {
            'fields': ('icon', 'image')
        }),
        ('Features', {
            'fields': ('features',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.created_by:
            obj.created_by = request.user
        return super().save_model(request, obj, form, change)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_at', 'author')
    list_filter = ('status', 'published_at')
    search_fields = ('title', 'content')
    exclude = ("author",)

   # save the author automatically according to the user who is logged in admin panel
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class EventGalleryImageInline(admin.TabularInline):
    model = EventGalleryImage
    extra = 1
    fields = ('image', 'caption', 'order')
    ordering = ('order', 'created_at')


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_at', 'ends_at', 'location', 'is_public')
    list_filter = ('starts_at', 'ends_at', 'is_public')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {"slug": ("title",)}
    inlines = [EventGalleryImageInline]


class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company_name',
                    'country', 'job_title', 'job_details', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'email', 'phone', 'company_name',
                     'country', 'job_title', 'job_details')


class InquiryResponseAdmin(admin.ModelAdmin):
    list_display = ('inquiry', 'sender_type', 'admin',
                    'recipient', 'subject', 'direction', 'sent_at')
    list_filter = ('sender_type', 'direction', 'sent_at')
    search_fields = ('inquiry__name', 'admin__username',
                     'recipient', 'subject', 'body')


# register models
admin.site.register(SoftwareSolution, SoftwareSolutionAdmin)
admin.site.register(CaseStudy, CaseStudyAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Inquiry, InquiryAdmin)
admin.site.register(InquiryResponse, InquiryResponseAdmin)
