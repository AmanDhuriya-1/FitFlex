from django.urls import path
from . import views

urlpatterns = [
    # -------- Home --------
    path('', views.home, name='home'),

    # -------- Clients --------
    path('clients/', views.client_list, name='client_list'),
    path('client/add/', views.add_client, name='add_client'),
    path('client/edit/<int:id>/', views.edit_client, name='edit_client'),
    path('client/delete/<int:id>/', views.delete_client, name='delete_client'),

    # -------- Workout Plans (Static Cards) --------
    path('plans/', views.plan_list, name='plan_list'),
    path('plans/assign/<int:plan_id>/', views.assign_plan, name='assign_plan'),

    # -------- Progress Tracker --------
    path('progress/', views.progress_list, name='progress_list'),
    path('progress/add/', views.add_progress, name='add_progress'),
    path('progress/edit/<int:id>/', views.edit_progress, name='edit_progress'),
    path('progress/delete/<int:id>/', views.delete_progress, name='delete_progress'),
]
