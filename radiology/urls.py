from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import(
                    create_radiology_service_view,
                    raise_patient_radiology_service_view,
                    desk_view,
                    pending_radiology_request_view,
                    radiology_request_detail_view,
                    send_radiology_results_view
                )   

urlpatterns = [
    path("create_radiology_service/", create_radiology_service_view, name="create_radiology_service"),
    path("raise_patient_radiology_service/<pid>/", raise_patient_radiology_service_view, name="raise_patient_radiology_service"),
    path("desk/<pid>/", desk_view, name="radiology_desk"),
    path("pending_rad_request/", pending_radiology_request_view, name="pending_rad_request"),
    path("radio_request_detail/<pid>", radiology_request_detail_view, name="radio_request_detail"),
    path("send_radiology_result/<request_id>", send_radiology_results_view, name="send_radiology_result"),
]