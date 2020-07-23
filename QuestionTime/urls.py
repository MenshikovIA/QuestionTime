from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django_registration.backends.one_step.views import RegistrationView

from users.forms import CustomUserForm
from core.views import IndexTemplateView


urlpatterns = [
    re_path('admin/', admin.site.urls),

    re_path('accounts/register/', RegistrationView.as_view(
        form_class=CustomUserForm,
        success_url='/'), name='django_registration_register'),

    re_path('accounts/', include('django_registration.backends.one_step.urls')),
    re_path('accounts/', include('django.contrib.auth.urls')),

    path('api/', include('users.api.urls')),
    path('api/', include('questions.api.urls')),

    path('api-auth/', include('rest_framework.urls')),
    path('api/rest-auth/', include('rest_auth.urls')),
    path('api/rest-auth/registration', include('rest_auth.registration.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
              [re_path("", IndexTemplateView.as_view(), name='entry-point'), ]
