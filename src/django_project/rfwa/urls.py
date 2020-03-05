from django.conf.urls import url
from django.urls import path, re_path
from rfwa import views

urlpatterns = [
    path('home/', views.index, name='index'),
    path('lectureslides/', views.lectureslides, name='lectureslides'),
    path('alllabs/', views.alllabs, name='alllabs'),
    path('workspace/', views.workspace, name='workspace'),
    path('register/', views.register, name='register'),
    path('feedback/', views.feedback, name='feedback'),
    path('summary/', views.summary, name='summary'),

    ##admin only
    path('manage/', views.manage, name='manage'),

    #labs
    path("manage_labs/", views.manage_labs, name="manage_labs"),
    path("add_lab/", views.add_lab, name="add_lab"),
    path("delete_lab/<str:labName>/", views.delete_lab, name='delete_lab'),
    path("unzip_lab/<str:labName>/", views.unzip_lab, name='unzip_lab'),

    #slides
    path("manage_slides/", views.manage_slides, name="manage_slides"),
    path("add_slide/", views.add_slide, name="add_slide"),
    path("delete_slide/<str:slideName>/", views.delete_slide, name='delete_slide'),
    
    #feedbacks
    path("manage_feedback/", views.manage_feedback, name="manage_feedback"),
    path("add_feedback/", views.add_feedback, name="add_feedback"),
    path("delete_feedback/<slug:slugName>/", views.delete_feedback, name='delete_feedback'),

    #display users
    path("view_users/", views.view_users, name="view_users"),
    
]