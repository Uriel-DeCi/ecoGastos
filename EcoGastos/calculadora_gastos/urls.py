from django.contrib import admin
from django.urls import path
from gastos import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Página de inicio
    path('', views.inicio, name='inicio'),
   

    # Opciones del menú
    path('gastos_mensuales/', views.gastos_mensuales, name='gastos_mensuales'),
    path('gastos_anuales/', views.gastos_anuales, name='gastos_anuales'),

    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login', views.login, name='login'),
    path('asesoria', views.asesoria, name='asesoria'),
    path('comparativas', views.comparativas, name='comparativas'),

    # Funcionalidades de la app
    
    path('exportar/', views.exportar_excel, name='exportar_excel'),
    path('exportar_excel_anual/', views.exportar_excel_anual, name='exportar_excel_anual'),
]
