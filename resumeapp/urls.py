

from . import views
from django.urls import path
urlpatterns = [
    path('resumes/',views.ResumeView.as_view()),
    path('resume/<str:pk>/',views.ResumeEditView.as_view()),
    path('addtoresume/<int:id>/',views.AddToResumeView.as_view(), name='add_to_resume'),
    path('myresume/',views.MyResumeView.as_view()),
    path('manageresume/<str:id>/',views.ManageResumeView.as_view()),
    path('candidate/<str:pk>/',views.CandidateView.as_view()),
    # path('checkout/',views.CheckoutView.as_view()),
]
# path('candidate/<str:pk>/',views.CandidateView.as_view()),
