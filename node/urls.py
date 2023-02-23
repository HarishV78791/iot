from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (home, 
                    project_api_write,viewProject,
                    plot_graph, register,project_list,
                    createProject, updateProject,
                    deleteProject, deleteConfirmProject,
                    UserPasswordChangeView,
                    UserPasswordResetView,
                    UserPasswordResetConfirmView)

urlpatterns =[
    path('',home,name='home'),
    path('projects/',project_list,name='project'),
    path('new_project/',createProject,name='new_project'),
    path('update_project/<int:pk>/',updateProject,name='update_project'),
    path('view_project/<int:pk>/',viewProject,name='view_project'),
    path('confirm_project_delete/<int:pk>/',deleteConfirmProject,name='confirm_delete_project'),
    path('final_delete_project/<int:pk>/',deleteProject,name='delete_project'),
    path('api_write/',project_api_write,name='api_write'),
    path('plot_graph/<int:pk>/',plot_graph,name='plot_graph'),
    path('login/',LoginView.as_view(template_name="login.html"),name='login'),
    path('logout/',LogoutView.as_view(template_name="logout.html"),name='logout'),
    path('register/',register,name='register'),
    path('password/change/', UserPasswordChangeView.as_view(), name='change_password'),
    path('password_reset/',UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]