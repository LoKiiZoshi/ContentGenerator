from django.contrib import admin
from django.urls import path
from contentgen_app .views import* 

urlpatterns = [
    path('admin/', admin.site.urls),
    
        path('', prompt_to_content_view, name='generate_content'),
] 