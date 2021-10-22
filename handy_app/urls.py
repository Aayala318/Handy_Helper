from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path("register", views.register),
    path("login", views.login),
    path("jobs", views.show_all),
    path("jobs/new", views.new_job),
    path("jobs/create", views.create_job),
    path("jobs/<int:job_id>", views.show_one),
    path("jobs/<int:job_id>/edit", views.edit),
    path("jobs/<int:job_id>/update", views.update),
    path("jobs/<int:job_id>/delete", views.delete),
    path("logout", views.logout)
]