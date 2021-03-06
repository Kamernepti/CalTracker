from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit', views.edit),
    path('create_food', views.add_food),
    path('add_exercise', views.add_exercise),
    path('profile', views.profile),
    path('add_weight', views.add_weight),
    path('meals/<int:meal_id>/destroy', views.remove_meal),
    path('meals/<int:meal_id>/edit', views.edit_food),  #working here
    path('meals/<int:meal_id>/update', views.update_food),
    path('exercises/<int:exercise_id>/destroy', views.remove_exercise),
    path('dashboard/prev_date', views.prev_date),
    path('dashboard/next_date', views.next_date),
    path('blogs', views.read_blogs),
    path('create_blog', views.create_blog)
]