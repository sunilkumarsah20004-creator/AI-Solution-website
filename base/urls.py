from django.urls import path
from .views import home, contact, case_study_list, case_studies_details, articles_page, articles_details, all_events_page, events_details
urlpatterns = [
    path('', home, name="home"),
    path('contact/', contact, name='contact'),
    path("case-study/", case_study_list, name="case-study"),
    path('case-studies/<slug:slug>/', case_studies_details,
         name="case_studies_details"),

    path('articles/', articles_page, name="articles"),
    path('articles/<slug:slug>/', articles_details, name="articles_details"),
    path('events/', all_events_page, name="events"),
    path('events/<slug:slug>/', events_details, name="events_details"),
]
