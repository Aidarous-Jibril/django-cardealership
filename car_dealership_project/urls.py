# urls.py in the main project directory 


from django.contrib import admin
from django.urls import path, include
from dealership.views import home_view  # Import the home view function
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Define URL pattern for the home page
    path('dealership/', include('dealership.urls')),
    path('auth/', include('authentication.urls', namespace='authentication')),
        

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    