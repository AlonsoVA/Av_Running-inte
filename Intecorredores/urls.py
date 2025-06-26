"""
URL configuration for Intecorredores project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from corredores import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='Homes'),
    path('h-info/', views.home2, name='Home2'),
    path('ruta/', views.ruta),
    path('rutapre/', views.rutapre),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login_view, name='login'),
    path('planes/', views.planes, name='planes'),
    path('usuario/', views.usuario, name='usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('usuario/info/<str:id>/', views.mostrar_usuario, name='infouser'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)