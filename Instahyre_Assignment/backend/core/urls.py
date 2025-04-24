from django.urls import path
from .views import RegisterView, LoginView, ContactListView, SpamReportListView,SpamCheckView ,SearchByNameView , SearchByPhoneNumberView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('contacts/', ContactListView.as_view(), name='contacts'),
    path('spam-reports/', SpamReportListView.as_view(), name='spam-reports'),
    path('check-spam/', SpamCheckView.as_view(), name='check-spam'),
    path('search/name/', SearchByNameView.as_view(), name='search-by-name'),
    path('search/phone/', SearchByPhoneNumberView.as_view(), name='search-by-phone'),
]
