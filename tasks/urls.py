from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),  # View to display the task list
    path('add/', views.add_task, name='add_task'),  # View to add a new task
    path('add/<int:task_id>/', views.add_task, name='edit_task'),  # View to edit a new task
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),  # View to delete a task
    path('pop_jokes/', views.pop_jokes, name='pop_jokes'),# View to pop_jokes 
    path('text_speech/', views.text_speech, name='text_speech'),# View to text_to_speech 
    # path('translator/', views.translator, name='translator'),
    path('generate-description/', views.generate_description, name='generate_description'),  # Add this

    path('mark_completed/<int:task_id>/', views.mark_completed, name='mark_completed'),  # Mark task as completed
]


