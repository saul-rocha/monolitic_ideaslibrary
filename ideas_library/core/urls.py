from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('settings/', views.settings, name='settings'),

    path('recomendar/', views.recomendar, name='recomendar'),

    path('recomendacoes/', views.recomendacoes, name='recomendacoes'),

    path('avaliacao/', views.avaliacao, name='avaliacao'),

    path('comentario/', views.comentario, name='comentario'),

    path('perfil/<str:pk>', views.perfil, name='perfil'),

    path('seguir', views.seguir, name='seguir'),

    path('buscar', views.buscar, name='buscar'),

    path('recomendacao/<str:pk>', views.recomendacao, name='recomendacao'),

    path('notifications', views.notifications, name='notifications'),

    path('cadastro/', views.cadastro, name='cadastro'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('home', views.home, name='home'),
]
