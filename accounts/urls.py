from django.urls import path
from . import views
urlpatterns = [
    path('UsersList/', views.get_students, name='get_students'),
    path('send-email/<str:email1>/<str:email2>/', views.send_email, name='send_email'),
    path('ProjectList/', views.ApiOverview, name='ApiOverview'),
    path('MyProjectList/<str:email>/', views.get_projects_by_user, name='get_projects_by_user'),
    path('ProjectList/create/', views.AddProject.as_view(), name='add-items'),
    path('ideas/create/', views.create_idea, name='create_idea'),
    path('ideas/', views.get_all_ideas, name='get_all_ideas'),
    path('update_profile/<str:email>/', views.update_profile, name='update_profile'),
    path('profile/<str:email>/', views.get_user_profile, name='get_user_profile'),
    path('ProjectList/all/', views.view_Projects, name='view_items'),
    path('upload-image/', views.upload_image, name='upload_image'),
    path('api/projects/upload/', views.ProjectUploadView.as_view(), name='project-upload'),
    path('user/<int:user_id>/', views.get_user_first_name, name='get_user_first_name'),
    path('ProjectList/delete/<int:project_id>/', views.delete_project, name='delete-project'),
    path('ProjectList/update/<int:project_id>/', views.AddProject.as_view(), name='update-items'),  
    path('ProjectList/category/<str:category>/',views.CategoryList.as_view(), name='projects-list-filtered'),
    path('ProjectList/category/filter',views.ProjectsViewSet.as_view(), name='filtring'),
    #regex = path(r'ProejctList/filter/(?P<category>Web-app|App|Arduino|Desktop App)/?(?P<year>[2-5]{1})/$', views.ProjectsViewSet.as_view(), name='filtring')
    #path('ProjectList/search/',views.search_projects, name='searching')
]