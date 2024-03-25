from django.urls import path
from .views import *

urlpatterns = [
    path('', Registration_View.as_view(), name="registration"),
    path('participantlist', ParticipantList_View.as_view(), name="participantlist"),
    path('spotregistration', SpotRegistration_View.as_view(), name="spotregistration"),
    path('import', import_csv_view, name="import"),
    path('registerparticipant', RegisterParticipant.as_view(), name="registerparticipant"),
    path('downloadcsv', download_csv, name="downloadcsv"),
    path('bytebattleunregister', BB_Unregister, name="bytebattleunregister"),
]
