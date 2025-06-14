from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),# to showcase your portfolio, use powerpoint, to do it like frontend, hero, about, projects(screenshots of postman and insomnia), contact, resume, blog, testimonials, skills, education, experience, certifications, awards, hobbies, interests, languages, references, pictures, details and links of all urls.
    path('api/', include('resumeapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

