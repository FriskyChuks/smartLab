from django.urls import path

from .views import single_user_reports_view, all_user_reports_view, clinical_reports_view

urlpatterns = [
    path('single_user_reports/<user_id>/', single_user_reports_view, name='single_user_reports'),
    path('all_user_reports/', all_user_reports_view, name='all_user_reports'),
    path('clinical_reports/', clinical_reports_view, name='clinical_reports'),
]