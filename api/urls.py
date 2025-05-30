from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('myapp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),]
# ]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

