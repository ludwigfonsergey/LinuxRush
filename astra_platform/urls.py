from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Админ панель
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', views.home, name='home'),
    
    # Аутентификация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Личный кабинет
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Уроки
    path('lessons/', views.lessons, name='lessons'),  # Список всех уроков
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),  # Конкретный урок
    
    # О проекте
    path('about/', views.about, name='about'),
    
    # Миссии (дополнительные страницы - можно реализовать позже)
    path('progress/', views.dashboard, name='progress'),  # Временный редирект
    path('achievements/', views.dashboard, name='achievements'),  # Временный редирект
    path('profile/', views.dashboard, name='profile'),  # Временный редирект
    
    # Миссии
    path('start-mission/<int:mission_id>/', views.start_mission, name='start_mission'),
    
    # Статические страницы (если понадобятся)
    # path('privacy/', views.privacy_policy, name='privacy'),
    # path('terms/', views.terms_of_service, name='terms'),
    
    # Встроенные Django представления для сброса пароля (если понадобится)
    # path('password-reset/', 
    #      auth_views.PasswordResetView.as_view(
    #          template_name='password_reset.html'
    #      ), 
    #      name='password_reset'),
    # path('password-reset/done/', 
    #      auth_views.PasswordResetDoneView.as_view(
    #          template_name='password_reset_done.html'
    #      ), 
    #      name='password_reset_done'),
    # path('password-reset-confirm/<uidb64>/<token>/', 
    #      auth_views.PasswordResetConfirmView.as_view(
    #          template_name='password_reset_confirm.html'
    #      ), 
    #      name='password_reset_confirm'),
    # path('password-reset-complete/', 
    #      auth_views.PasswordResetCompleteView.as_view(
    #          template_name='password_reset_complete.html'
    #      ), 
    #      name='password_reset_complete'),
]

# Добавляем статические файлы для разработки
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Обработчик для страницы 404 (если нужно)
# handler404 = 'astra_platform.views.handler404'

# Обработчик для страницы 500 (если нужно)
# handler500 = 'astra_platform.views.handler500'